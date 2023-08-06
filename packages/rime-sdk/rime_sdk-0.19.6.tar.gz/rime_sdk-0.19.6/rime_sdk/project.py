"""Library defining the interface to a project."""
import json
from datetime import datetime, timedelta
from typing import Any, Dict, Iterator, List, NamedTuple, Optional, Tuple, cast

import grpc
from google.protobuf.timestamp_pb2 import Timestamp

from rime_sdk.firewall import (
    Firewall,
    get_reference_set_source,
    location_args_to_data_location,
)
from rime_sdk.internal.backend import RIMEBackend
from rime_sdk.internal.config_parser import convert_config_to_proto
from rime_sdk.internal.proto_utils import (
    get_bin_size_proto,
    get_data_type_enum,
    get_threshold_info_proto,
)
from rime_sdk.internal.utils import convert_dict_to_html, make_link
from rime_sdk.protos.notification.notification_pb2 import (
    CreateNotificationRequest,
    DeleteNotificationRequest,
    DigestConfig,
    JobActionConfig,
    ListNotificationsRequest,
    ListNotificationsResponse,
    MonitoringConfig,
    Notification,
    NotificationType,
    UpdateNotificationRequest,
    WebhookConfig,
)
from rime_sdk.protos.project.project_pb2 import (
    AnnotatedProject,
    DeleteProjectRequest,
    GetProjectRequest,
)
from rime_sdk.protos.ri.api.featureflag.feature_flag_pb2 import (
    GetLimitStatusRequest,
    LicenseLimit,
    LimitStatus,
)
from rime_sdk.protos.ri.api.firewall.firewall_pb2 import (
    ConvertIDsRequest,
    ConvertIDsResponse,
    CreateFirewallFromComponentsRequest,
    CreateFirewallFromTestRunIDRequest,
    CreateFirewallResponse,
    FirewallComponents,
    FirewallConvIDType,
    FirewallRules,
)
from rime_sdk.protos.ri.api.resultsynthesizer.result_message_pb2 import (  # pylint: disable=unused-import
    DataType,
)
from rime_sdk.protos.ri.api.testrunresults.test_run_results_pb2 import (
    GetTestRunRequest,
    GetTestRunResponse,
    ListTestRunsRequest,
    ListTestRunsResponse,
)
from rime_sdk.test_run import TestRun

NOTIFICATION_TYPE_JOB_ACTION_STR: str = "Job_Action"
NOTIFICATION_TYPE_MONITORING_STR: str = "Monitoring"
NOTIFICATION_TYPE_DIGEST_STR: str = "Daily_Digest"
NOTIFICATION_TYPE_UNSPECIFIED_STR: str = "Unspecified"
NOTIFICATION_TYPES_STR_LIST: List[str] = [
    NOTIFICATION_TYPE_JOB_ACTION_STR,
    NOTIFICATION_TYPE_MONITORING_STR,
    NOTIFICATION_TYPE_DIGEST_STR,
]


class ProjectInfo(NamedTuple):
    """This object contains static information that describes a project."""

    project_id: str
    """How to refer to the project in the backend."""
    name: str
    """Name of the project."""
    description: str
    """Description of the project"""


class Project:
    """An interface to a RIME project.

    This object provides an interface for editing, updating, and deleting projects.

    Attributes:
        backend: RIMEBackend
            The RIME backend used to query about the status of the job.
        project_id: str
            The identifier for the RIME project that this object monitors.
    """

    def __init__(self, backend: RIMEBackend, project_id: str) -> None:
        """Contains information about a RIME Project.

        Args:
            backend: RIMEBackend
                The RIME backend used to query about the status of the job.
            project_id: str
                The identifier for the RIME project that this object monitors.
        """
        self._backend = backend
        self._project_id = project_id

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"Project({self._project_id})"

    def _repr_html_(self) -> str:
        """Return HTML representation of the object."""
        info = {
            "Project ID": self._project_id,
            "Link": make_link("https://" + self.get_link(), link_text="Project Page"),
        }
        return convert_dict_to_html(info)

    @property
    def project_id(self) -> str:
        """Return the id of this project."""
        return self._project_id

    def _check_firewall_creation_limit(self) -> None:
        """Check if creating another firewall would be within license limits.

        Raises:
            ValueError if another firewall cannot be created as it would
            exceed license limits.
        """
        req = GetLimitStatusRequest(
            customer_name=self._backend.customer_name,
            limit=LicenseLimit.LICENSE_LIMIT_FIREWALL,
        )
        with self._backend.get_feature_flag_stub() as feature_flag_client:
            with self._backend.GRPCErrorHandler():
                feature_flag_response = feature_flag_client.GetLimitStatus(req)

        limit_status = feature_flag_response.limit_status.limit_status
        limit_value = feature_flag_response.limit_status.limit_value
        if limit_status == LimitStatus.Status.WARN:
            curr_value = feature_flag_response.limit_status.current_value
            print(
                f"You are approaching the limit ({curr_value + 1}"
                f"/{limit_value}) of models monitored. Contact the"
                f" Robust Intelligence team to upgrade your license."
            )
        elif limit_status == LimitStatus.Status.ERROR:
            # could be either within grace period or exceeded grace period
            # if the latter, let the create firewall call raise the
            # error
            print(
                "You have reached the limit of models monitored."
                " Contact the Robust Intelligence team to"
                " upgrade your license."
            )
        elif limit_status == LimitStatus.Status.OK:
            pass
        else:
            raise ValueError("Unexpected status value.")

    def _get_data_type(self, test_run_id: str) -> "DataType.V":
        """Get the Data Type associated with this test run."""
        req = GetTestRunRequest(test_run_id=test_run_id)
        with self._backend.GRPCErrorHandler():
            with self._backend.get_test_run_results_stub() as results_reader:
                res: GetTestRunResponse = results_reader.GetTestRun(req)
        return res.test_run.data_type

    def _get_project(self) -> AnnotatedProject:
        """Get the project info from the backend.

        Returns:
            A ``GetProjectResponse`` object.
        """
        req = GetProjectRequest(project_id=self._project_id)
        with self._backend.get_project_manager_stub() as project_client:
            with self._backend.GRPCErrorHandler():
                response = project_client.GetProject(req)
        return response.project

    @property
    def info(self) -> ProjectInfo:
        """Return information about this project."""
        project = self._get_project()
        return ProjectInfo(
            self._project_id, project.project.name, project.project.description,
        )

    def get_link(self) -> str:
        """Get the web app URL to the project.

        This link directs to your organization's deployment of RIME.
        You can view more detailed information in the web app, including
        information on your test runs, comparisons of those results,
        and models that are monitored.

        Note: this is a string that should be copy-pasted into a browser.
        """
        project = self._get_project()
        return project.web_app_url.url

    @property
    def name(self) -> str:
        """Return the name of this project."""
        return self.info.name

    @property
    def description(self) -> str:
        """Return the description of this project."""
        return self.info.description

    def list_test_runs(self) -> Iterator[TestRun]:
        """List the stress test runs associated with the project."""
        with self._backend.get_test_run_results_stub() as test_run_results:
            # Iterate through the pages of projects and break at the last page.
            page_token = ""
            while True:
                if page_token == "":
                    request = ListTestRunsRequest(project_id=self._project_id,)
                else:
                    request = ListTestRunsRequest(page_token=page_token)
                res: ListTestRunsResponse = test_run_results.ListTestRuns(request)
                for test_run in res.test_runs:
                    yield TestRun(self._backend, test_run.test_run_id)
                # Advance to the next page of test cases.
                page_token = res.next_page_token
                # we've reached the last page of test cases.
                if not res.has_more:
                    break

    def create_firewall(
        self,
        name: str,
        bin_size: str,
        test_run_id: str,
        run_ct_schedule: bool = False,
        rolling_window_duration: Optional[timedelta] = None,
        reference_set_time_bin: Optional[Tuple[datetime, datetime]] = None,
        location_type: Optional[str] = None,
        location_info: Optional[Dict] = None,
        data_params: Optional[Dict] = None,
        rime_managed_image: Optional[str] = None,
    ) -> Firewall:  # noqa: D400, D402
        """Create a Firewall for a given project.

        Args:
            name: str
                FW name.
            bin_size: str
                Bin size. Can be `year`, `month`, `week`, `day`, `hour`.
            test_run_id: str
                ID of the stress test run that firewall will be based on.
            run_ct_schedule: bool
                Flag for ct scheduler.
            rolling_window_duration: Optional[int]
                Time duration of rolling window of reference set if provided.
                The rolling window is only supported for firewall running scheduled ct.
                Only one of rolling_window_seconds or reference_set_time_bin may be set.
            reference_set_time_bin: Optional[Tuple[datetime, datetime]]
                Time bin of reference set can be set for firewall running scheduled ct.
                Only one of rolling_window_seconds or reference_set_time_bin may be set.
            location_type: Optional[str]
                Type of the data location that ScheduledCT will pull data from.
            location_info: Optional[Dict]
                Information needed to access the data location provided.
            data_params: Optional[Dict]
                Information needed to process data from the data location provided.
                By default, these are obtained from your reference information.
                Eg. `pred_col`, `timestamp_col`, `label_col`, etc...
            rime_managed_image: Optional[str]
                Name of a managed image to use when running the model test.
                The image must have all dependencies required by your model. To create
                new managed images with your desired dependencies, use the client's
                ``create_managed_image()`` method.


        Returns:
            A ``Firewall`` object.

        Raises:
            ValueError
                If the provided values are invalid.
                If the request to the Firewall service failed.

        Example:

        .. code-block:: python

            # Create FW based on foo stress test in project.
            firewall = project.create_firewall(
                "firewall name", "day", "foo")
        """
        self._check_firewall_creation_limit()
        bin_size_proto = get_bin_size_proto(bin_size_str=bin_size)
        reference_set_source = get_reference_set_source(
            rolling_window_duration=rolling_window_duration,
            reference_set_time_bin=reference_set_time_bin,
        )
        req = CreateFirewallFromTestRunIDRequest(
            name=name,
            project_id=self._project_id,
            bin_size=bin_size_proto,
            run_ct_schedule=run_ct_schedule,
            stress_test_run_id=test_run_id,
            reference_set_source=reference_set_source,
        )

        if rime_managed_image:
            req.managed_image.name = rime_managed_image

        # Prevent location info from being provided without location type
        if location_info is not None and location_type is None:
            raise ValueError("Must Specify both location type and location info.")
        if location_type is not None:
            data_type = self._get_data_type(test_run_id)
            location_args = location_args_to_data_location(
                location_type, location_info, data_params, data_type
            )
            req.data_location_info.CopyFrom(location_args)
        try:
            with self._backend.get_firewall_stub() as firewall_tester:
                res = firewall_tester.CreateFirewallFromTestRunID(req)
                res = cast(CreateFirewallResponse, res)
                return Firewall(self._backend, res.firewall_id)
        except grpc.RpcError as rpc_error:
            if rpc_error.code() == grpc.StatusCode.NOT_FOUND:
                raise ValueError(
                    f"a test run with this id (`{test_run_id}`)  does not exist"
                )
            raise ValueError(rpc_error.details()) from None

    def create_firewall_from_components(
        self,
        name: str,
        bin_size: str,
        stress_test_config: Dict[str, Any],
        firewall_rules: List[Dict[str, Any]],
        threshold_infos: List[dict],
        run_ct_schedule: bool = False,
        location_type: Optional[str] = None,
        location_info: Optional[Dict] = None,
        data_params: Optional[Dict] = None,
        rime_managed_image: Optional[str] = None,
        data_type: str = "tabular",
    ) -> Firewall:  # noqa: D400, D402
        """Create a Firewall for a given project.

        Args:
            name: str
                FW name.
            bin_size: str
                Can be `year`, `month`, `week`, `day`, `hour`.
            stress_test_config: dict
                RIME Config that indicates the testing, model, and data configurations
            firewall_rules: List[Dict]
                Firewall Rules to update the firewall with.
            threshold_infos: List[Dict]
                Threshold info for each summary metric.
            run_ct_schedule: bool
                Flag for ct scheduler.
            location_type: Optional[str]
                Type of the data location that ScheduledCT will pull data from.
            location_info:  Optional[Dict]
                Information needed to access the data location provided.
            data_params: Optional[Dict]
                Information needed to process data from the data location provided.
                By default, these are obtained from your reference information.
                Eg. `pred_col`, `timestamp_col`, `label_col`, etc...
            rime_managed_image: Optional[str]
                Name of a managed image to use when running the model test.
                The image must have all dependencies required by your model. To create
                new managed images with your desired dependencies, use the client's
                ``create_managed_image()`` method.
            data_type: str
                Type of data this firewall test is to be run on. Should be one of
                `tabular`, `nlp`, `images`. Defaults to `tabular`.


        Returns:
            A ``Firewall`` object.

        Raises:
            ValueError
                If the provided values are invalid.
                If the request to the Firewall service failed.

        Example:

        .. code-block:: python

            # Create FW manually from components.
           stress_test_config = {
                "data_info": {
                    "pred_col": "preds",
                    "label_col": "label",
                    "ref_path": "s3://my-bucket/my-data.csv",
                },
                "model_info": {"path": "s3://model-test-bucket/model.py",},
                "model_task": "Binary Classification",
            }
            firewall_rules = [
                {
                    "test_name": "Unseen Categorical",
                    "description": "Value must be in a required set of values",
                    "is_transformation": False,
                    "firewall_configs": [
                        {
                            "rule_info": {
                                "feature_names": ["city"],
                                "flagged_action": "FLAG",
                            }
                        }
                    ],
                }
            ]
            metric_thresholds = [
                {
                    "direction": "below",
                    "low": 0.999,
                    "medium": 0.99,
                    "high": 0.9,
                    "metric_name": "accuracy",
                }
            ]
            firewall = project.create_firewall_from_components(
                "firewall name",
                "day",
                stress_test_config,
                firewall_rules,
                metric_thresholds,
            )
        """
        bin_size_proto = get_bin_size_proto(bin_size_str=bin_size)
        proto_data_type = get_data_type_enum(data_type)
        typed_cli_config = convert_config_to_proto(stress_test_config, proto_data_type)
        firewall_rules_pb = FirewallRules(
            data=json.dumps(firewall_rules).encode("utf-8")
        )
        metric_thresholds = [
            get_threshold_info_proto(threshold_dict)
            for threshold_dict in threshold_infos
        ]
        req = CreateFirewallFromComponentsRequest(
            name=name,
            project_id=self._project_id,
            bin_size=bin_size_proto,
            run_ct_schedule=run_ct_schedule,
            components=FirewallComponents(
                typed_cli_config=typed_cli_config,
                firewall_rules=firewall_rules_pb,
                threshold_infos=metric_thresholds,
            ),
        )

        if rime_managed_image:
            req.managed_image.name = rime_managed_image

        # Prevent location info from being provided without location type
        if location_info is not None and location_type is None:
            raise ValueError("Must Specify both location type and location info.")
        if location_type is not None:
            location_args = location_args_to_data_location(
                location_type, location_info, data_params, proto_data_type
            )
            req.data_location_info.CopyFrom(location_args)
        with self._backend.GRPCErrorHandler():
            with self._backend.get_firewall_stub() as firewall_tester:
                res = firewall_tester.CreateFirewallFromComponents(req)
                res = cast(CreateFirewallResponse, res)
                return Firewall(self._backend, res.firewall_id)

    def _get_firewall_id(self) -> Optional[str]:
        src_type = FirewallConvIDType.FIREWALL_CONV_ID_TYPE_PROJECT_ID
        dst_type = FirewallConvIDType.FIREWALL_CONV_ID_TYPE_FIREWALL_ID
        req = ConvertIDsRequest(
            src_type=src_type, dst_type=dst_type, src_ids=[self._project_id]
        )
        with self._backend.GRPCErrorHandler():
            with self._backend.get_firewall_stub() as firewall_tester:
                res: ConvertIDsResponse = firewall_tester.ConvertIDs(req)
        src_dst_id_mapping = res.src_dst_id_mapping
        if self._project_id not in src_dst_id_mapping:
            return None
        # Current backend functionality is to return mapping for everything,
        # but with empty string if no firewall exists.
        firewall_id = src_dst_id_mapping.get(self._project_id, "")
        if firewall_id == "":
            return None
        return firewall_id

    def get_firewall(self) -> Firewall:
        """Get the active Firewall for a project if it exists.

        Query the backend for an active `Firewall` in this project which
        can be used to perform Firewall operations. If there is no active
        Firewall for the project, this call will error.

        Returns:
            A ``Firewall`` object.

        Raises:
            ValueError
                If the Firewall does not exist.

        Example:

        .. code-block:: python

            # Get FW if it exists.
            firewall = project.get_firewall()
        """
        firewall_id = self._get_firewall_id()
        if firewall_id is None:
            raise ValueError("No firewall found for given project.")
        return Firewall(self._backend, firewall_id)

    def has_firewall(self) -> bool:
        """Check whether a project has a firewall or not."""
        firewall_id = self._get_firewall_id()
        return firewall_id is not None

    def delete_firewall(self) -> None:
        """Delete firewall for this project if exists."""
        firewall = self.get_firewall()
        firewall.delete_firewall()

    def _list_notification_settings(self) -> ListNotificationsResponse:
        """Get list of notifications associated with the current project."""
        req = ListNotificationsRequest(
            list_notifications_query=ListNotificationsRequest.ListNotificationsQuery(
                notification_object_ids=[self.project_id],
            )
        )
        with self._backend.get_notification_settings_stub() as notif_stub:
            res = notif_stub.ListNotifications(req)
            return res

    def _set_create_notification_setting_config_from_type(
        self, req: CreateNotificationRequest, notif_type: int
    ) -> None:
        if notif_type == NotificationType.NOTIFICATION_TYPE_JOB_ACTION:
            req.config.job_action.CopyFrom(JobActionConfig())
        elif notif_type == NotificationType.NOTIFICATION_TYPE_MONITORING:
            req.config.monitoring_config.CopyFrom(MonitoringConfig())
        elif notif_type == NotificationType.NOTIFICATION_TYPE_DIGEST:
            timestamp = Timestamp()
            timestamp.GetCurrentTime()
            req.config.digest_config.CopyFrom(
                DigestConfig(frequency=DigestConfig.DAILY)
            )

    def _get_notification_type_from_str(self, notif_type: str) -> int:
        if notif_type == NOTIFICATION_TYPE_JOB_ACTION_STR:
            return NotificationType.NOTIFICATION_TYPE_JOB_ACTION
        elif notif_type == NOTIFICATION_TYPE_MONITORING_STR:
            return NotificationType.NOTIFICATION_TYPE_MONITORING
        elif notif_type == NOTIFICATION_TYPE_DIGEST_STR:
            return NotificationType.NOTIFICATION_TYPE_DIGEST
        else:
            raise ValueError(
                f"Notification type must be one of {NOTIFICATION_TYPES_STR_LIST}"
            )

    def _get_notification_type_str(self, notif_type: int) -> str:
        if notif_type == NotificationType.NOTIFICATION_TYPE_JOB_ACTION:
            return NOTIFICATION_TYPE_JOB_ACTION_STR
        elif notif_type == NotificationType.NOTIFICATION_TYPE_MONITORING:
            return NOTIFICATION_TYPE_MONITORING_STR
        elif notif_type == NotificationType.NOTIFICATION_TYPE_DIGEST:
            return NOTIFICATION_TYPE_DIGEST_STR
        else:
            # This function is called only to show the user notification types
            # as string as defined in NOTIFICATION_TYPES_STR_LIST. We will have
            # to update this if we add more notification types in the future.
            # Making it unspecified will not break any SDK/BE mismatch and still
            # show users the new notification type with unspecified tag.
            # This situation should not happen ideally
            return NOTIFICATION_TYPE_UNSPECIFIED_STR

    def get_notification_settings(self) -> Dict:
        """Get the list of notifications for the project.

        Queries the backend to get a list of notifications
        added to the project. The notifications are grouped by the type
        of the notification and each type contains a list of emails and webhooks
        which are added to the notification setting

        Returns:
            A Dictionary of notification type and corresponding
            emails and webhooks added for that notification type.

        Example:

        .. code-block:: python

            notification_settings = project.list_notification_settings()
        """
        notif_list = self._list_notification_settings()
        out: Dict = {}
        for notif in notif_list.notifications:
            notif_type_str = self._get_notification_type_str(notif.notification_type)
            out[notif_type_str] = {}
            out[notif_type_str]["emails"] = notif.emails
            out[notif_type_str]["webhooks"] = []
            for webhook in notif.webhooks:
                out[notif_type_str]["webhooks"].append(webhook.webhook)
        return out

    def _add_notif_entry(
        self,
        notif_type_str: str,
        email: Optional[str],
        webhook_config: Optional[WebhookConfig],
    ) -> None:
        """Add the email or webhook in the notification settings of notif_type.

        This function should be called with either one of an email or a webhook
        to be added in a single call. emails are checked first and we add a
        webhook only when email is set to None. The function first checks if
        a notification object exists for the give notification type and appends
        the email/webhook if found, else it creates a new notification object
        """
        if email is not None and webhook_config is not None:
            raise ValueError(
                "_add_notif_entry expects exactly one of email or "
                "webhook config to be set"
            )
        notif_setting_list = self._list_notification_settings()
        notif_type = self._get_notification_type_from_str(notif_type_str)
        for notif_setting in notif_setting_list.notifications:
            if notif_setting.notification_type == notif_type:
                if email is not None:
                    for existing_email in notif_setting.emails:
                        if existing_email == email:
                            print(
                                f"Email: {email} already exists in notification "
                                f"settings for notification type: {notif_type_str}"
                            )
                            return
                    notif_setting.emails.append(email)
                elif webhook_config is not None:
                    for existing_webhook in notif_setting.webhooks:
                        if existing_webhook.webhook == webhook_config.webhook:
                            print(
                                f"Webhook: {webhook_config.webhook} "
                                "already exists in notification settings "
                                f"for notification type: {notif_type_str}"
                            )
                            return
                    notif_setting.webhooks.append(webhook_config)
                update_req = UpdateNotificationRequest(notification=notif_setting)
                with self._backend.get_notification_settings_stub() as notif_stub:
                    notif_stub.UpdateNotification(update_req)
                return
        # Notification setting does not exist for the notif_type.
        req = CreateNotificationRequest(
            notification_object_type=Notification.PROJECT,
            notification_object_id=self.project_id,
        )
        self._set_create_notification_setting_config_from_type(req, notif_type)
        notif_entry_str = ""
        if email is not None:
            req.emails.append(email)
            notif_entry_str = "Email " + email
        elif webhook_config is not None:
            req.webhooks.append(webhook_config)
            notif_entry_str = "Webhook " + webhook_config.webhook
        with self._backend.get_notification_settings_stub() as notif_stub:
            notif_stub.CreateNotification(req)
        print(f"{notif_entry_str} added for notification type {notif_type_str}")

    def _remove_notif_entry(
        self,
        notif_type_str: str,
        email: Optional[str],
        webhook_config: Optional[WebhookConfig],
    ) -> None:
        """Remove the email or webhook in the notification settings of notif_type.

        This function should be called with either one of an email or a webhook
        to be removed in a single call. emails are checked first and we remove
        webhook only when email is set to None. In case a delete operation
        leads to the notification object having no email or webhook, that
        notification object is deleted as well.
        """
        if email is not None and webhook_config is not None:
            raise ValueError(
                "_remove_notif_entry expects exactly one of email "
                "or webhook config to be set"
            )
        notif_setting_list = self._list_notification_settings()
        notif_type = self._get_notification_type_from_str(notif_type_str)
        for notif_setting in notif_setting_list.notifications:
            if notif_setting.notification_type == notif_type:
                found = False
                if email is not None:
                    for existing_email in notif_setting.emails:
                        if existing_email == email:
                            notif_setting.emails.remove(existing_email)
                            found = True
                elif webhook_config is not None:
                    for existing_webhook in notif_setting.webhooks:
                        if existing_webhook.webhook == webhook_config.webhook:
                            notif_setting.webhooks.remove(existing_webhook)
                            found = True
                if found:
                    if (
                        len(notif_setting.emails) == 0
                        and len(notif_setting.webhooks) == 0
                    ):
                        del_req = DeleteNotificationRequest(id=notif_setting.id)
                        with self._backend.get_notification_settings_stub() as notif_s:
                            notif_s.DeleteNotification(del_req)
                    else:
                        update_req = UpdateNotificationRequest(
                            notification=notif_setting
                        )
                        with self._backend.get_notification_settings_stub() as notif_s:
                            notif_s.UpdateNotification(update_req)
                    return
        notif_entry_str = ""
        if email is not None:
            notif_entry_str = "Email " + email
        elif webhook_config is not None:
            notif_entry_str = "Webhook " + webhook_config.webhook
        print(f"{notif_entry_str} not found for notification type {notif_type_str}")

    def add_email(self, email: str, notif_type_str: str) -> None:
        # pylint: disable=line-too-long
        """Add an email to the notification settings for the given notification type.

        Currently, we support 3 notification types:
        ["Job_Action", "Monitoring", "Daily_Digest"]

        Example:
            .. code-block:: python

                notification_settings = project.add_email("<email>", "<notification type>")
        """
        if email == "":
            raise ValueError("Email must be a non empty string")
        return self._add_notif_entry(
            notif_type_str=notif_type_str, email=email, webhook_config=None
        )

    def remove_email(self, email: str, notif_type_str: str) -> None:
        # pylint: disable=line-too-long
        """Remove an email from notification settings for the given notification type.

        Currently, we support 3 notification types:
        ["Job_Action", "Monitoring", "Daily_Digest"]

        Example:
            .. code-block:: python

                notification_settings = project.remove_email("<email>", "<notification type>")
        """
        if email == "":
            raise ValueError("Email must be a non empty string")
        return self._remove_notif_entry(
            notif_type_str=notif_type_str, email=email, webhook_config=None
        )

    def add_webhook(self, webhook: str, notif_type_str: str) -> None:
        # pylint: disable=line-too-long
        """Add a webhook to the notification settings for the given notification type.

        Currently, we support 3 notification types:
        ["Job_Action", "Monitoring", "Daily_Digest"]

        Example:
            .. code-block:: python

                notification_settings = project.add_webhook("<webhook>", "<notification type>")
        """
        if webhook == "":
            raise ValueError("Webhook must be a non empty string")
        webhook_config = WebhookConfig(webhook=webhook)
        return self._add_notif_entry(
            notif_type_str=notif_type_str, email=None, webhook_config=webhook_config
        )

    def remove_webhook(self, webhook: str, notif_type_str: str) -> None:
        # pylint: disable=line-too-long,
        """Remove a webhook from notification settings for the given notification type.

        Currently, we support 3 notification types:
        ["Job_Action", "Monitoring", "Daily_Digest"]

        Example:
            .. code-block:: python

                notification_settings = project.remove_webhook("<webhook>", "<notification type>")
        """
        if webhook == "":
            raise ValueError("Webhook must be a non empty string")
        webhook_config = WebhookConfig(webhook=webhook)
        return self._remove_notif_entry(
            notif_type_str=notif_type_str, email=None, webhook_config=webhook_config
        )

    def delete(self) -> None:
        """Delete project in RIME's backend."""
        req = DeleteProjectRequest(project_id=self._project_id)
        try:
            with self._backend.get_project_manager_stub() as project_manager:
                project_manager.DeleteProject(request=req)
        except grpc.RpcError as rpc_error:
            if rpc_error.code() == grpc.StatusCode.NOT_FOUND:
                raise ValueError(
                    f"project with this id {self._project_id} does not exist"
                )
            raise ValueError(rpc_error.details()) from None
