'''
# CDK Construct for S3 Bucket Replication

A CDK Construct for S3 Bucket Replication.  Can handle cross-account replication.  Make sure the source and destination buckets have versioning enabled.

```
const sourceBucket = new Bucket(this, 'SourceBucket', {
  versioned: true,
});
const destinationBucket = new Bucket(this, 'DestinationBucket', {
  versioned: true,
});

new BucketReplication(this, 'BucketReplication', {
  sourceBucket,
  destinationBucket,
  replicationDestinationProperties: {
    storageClass: ReplicationDestinationStorageClass.STANDARD_IA,
  },
});
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk.aws_s3
import aws_cdk.core


class BucketReplication(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-s3-bucketreplication.BucketReplication",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        destination_bucket: aws_cdk.aws_s3.IBucket,
        source_bucket: aws_cdk.aws_s3.IBucket,
        replication_destination_properties: typing.Optional[typing.Union["ReplicationDestinationPropertyNoBucket", typing.Dict[str, typing.Any]]] = None,
        replication_rule_properties: typing.Optional[typing.Union["ReplicationRulePropertyNoDestination", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param destination_bucket: 
        :param source_bucket: 
        :param replication_destination_properties: 
        :param replication_rule_properties: 
        '''
        if __debug__:
            def stub(
                scope: aws_cdk.core.Construct,
                id: builtins.str,
                *,
                destination_bucket: aws_cdk.aws_s3.IBucket,
                source_bucket: aws_cdk.aws_s3.IBucket,
                replication_destination_properties: typing.Optional[typing.Union["ReplicationDestinationPropertyNoBucket", typing.Dict[str, typing.Any]]] = None,
                replication_rule_properties: typing.Optional[typing.Union["ReplicationRulePropertyNoDestination", typing.Dict[str, typing.Any]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = BucketReplicationProps(
            destination_bucket=destination_bucket,
            source_bucket=source_bucket,
            replication_destination_properties=replication_destination_properties,
            replication_rule_properties=replication_rule_properties,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-s3-bucketreplication.BucketReplicationProps",
    jsii_struct_bases=[],
    name_mapping={
        "destination_bucket": "destinationBucket",
        "source_bucket": "sourceBucket",
        "replication_destination_properties": "replicationDestinationProperties",
        "replication_rule_properties": "replicationRuleProperties",
    },
)
class BucketReplicationProps:
    def __init__(
        self,
        *,
        destination_bucket: aws_cdk.aws_s3.IBucket,
        source_bucket: aws_cdk.aws_s3.IBucket,
        replication_destination_properties: typing.Optional[typing.Union["ReplicationDestinationPropertyNoBucket", typing.Dict[str, typing.Any]]] = None,
        replication_rule_properties: typing.Optional[typing.Union["ReplicationRulePropertyNoDestination", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param destination_bucket: 
        :param source_bucket: 
        :param replication_destination_properties: 
        :param replication_rule_properties: 
        '''
        if isinstance(replication_destination_properties, dict):
            replication_destination_properties = ReplicationDestinationPropertyNoBucket(**replication_destination_properties)
        if isinstance(replication_rule_properties, dict):
            replication_rule_properties = ReplicationRulePropertyNoDestination(**replication_rule_properties)
        if __debug__:
            def stub(
                *,
                destination_bucket: aws_cdk.aws_s3.IBucket,
                source_bucket: aws_cdk.aws_s3.IBucket,
                replication_destination_properties: typing.Optional[typing.Union["ReplicationDestinationPropertyNoBucket", typing.Dict[str, typing.Any]]] = None,
                replication_rule_properties: typing.Optional[typing.Union["ReplicationRulePropertyNoDestination", typing.Dict[str, typing.Any]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument destination_bucket", value=destination_bucket, expected_type=type_hints["destination_bucket"])
            check_type(argname="argument source_bucket", value=source_bucket, expected_type=type_hints["source_bucket"])
            check_type(argname="argument replication_destination_properties", value=replication_destination_properties, expected_type=type_hints["replication_destination_properties"])
            check_type(argname="argument replication_rule_properties", value=replication_rule_properties, expected_type=type_hints["replication_rule_properties"])
        self._values: typing.Dict[str, typing.Any] = {
            "destination_bucket": destination_bucket,
            "source_bucket": source_bucket,
        }
        if replication_destination_properties is not None:
            self._values["replication_destination_properties"] = replication_destination_properties
        if replication_rule_properties is not None:
            self._values["replication_rule_properties"] = replication_rule_properties

    @builtins.property
    def destination_bucket(self) -> aws_cdk.aws_s3.IBucket:
        result = self._values.get("destination_bucket")
        assert result is not None, "Required property 'destination_bucket' is missing"
        return typing.cast(aws_cdk.aws_s3.IBucket, result)

    @builtins.property
    def source_bucket(self) -> aws_cdk.aws_s3.IBucket:
        result = self._values.get("source_bucket")
        assert result is not None, "Required property 'source_bucket' is missing"
        return typing.cast(aws_cdk.aws_s3.IBucket, result)

    @builtins.property
    def replication_destination_properties(
        self,
    ) -> typing.Optional["ReplicationDestinationPropertyNoBucket"]:
        result = self._values.get("replication_destination_properties")
        return typing.cast(typing.Optional["ReplicationDestinationPropertyNoBucket"], result)

    @builtins.property
    def replication_rule_properties(
        self,
    ) -> typing.Optional["ReplicationRulePropertyNoDestination"]:
        result = self._values.get("replication_rule_properties")
        return typing.cast(typing.Optional["ReplicationRulePropertyNoDestination"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BucketReplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-s3-bucketreplication.ReplicationDestinationPropertyNoBucket",
    jsii_struct_bases=[],
    name_mapping={
        "access_control_translation": "accessControlTranslation",
        "account": "account",
        "encryption_configuration": "encryptionConfiguration",
        "metrics": "metrics",
        "replication_time": "replicationTime",
        "storage_class": "storageClass",
    },
)
class ReplicationDestinationPropertyNoBucket:
    def __init__(
        self,
        *,
        access_control_translation: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union[aws_cdk.aws_s3.CfnBucket.AccessControlTranslationProperty, typing.Dict[str, typing.Any]]]] = None,
        account: typing.Optional[builtins.str] = None,
        encryption_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union[aws_cdk.aws_s3.CfnBucket.EncryptionConfigurationProperty, typing.Dict[str, typing.Any]]]] = None,
        metrics: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union[aws_cdk.aws_s3.CfnBucket.MetricsProperty, typing.Dict[str, typing.Any]]]] = None,
        replication_time: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union[aws_cdk.aws_s3.CfnBucket.ReplicationTimeProperty, typing.Dict[str, typing.Any]]]] = None,
        storage_class: typing.Optional["ReplicationDestinationStorageClass"] = None,
    ) -> None:
        '''
        :param access_control_translation: 
        :param account: 
        :param encryption_configuration: 
        :param metrics: 
        :param replication_time: 
        :param storage_class: 
        '''
        if __debug__:
            def stub(
                *,
                access_control_translation: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union[aws_cdk.aws_s3.CfnBucket.AccessControlTranslationProperty, typing.Dict[str, typing.Any]]]] = None,
                account: typing.Optional[builtins.str] = None,
                encryption_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union[aws_cdk.aws_s3.CfnBucket.EncryptionConfigurationProperty, typing.Dict[str, typing.Any]]]] = None,
                metrics: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union[aws_cdk.aws_s3.CfnBucket.MetricsProperty, typing.Dict[str, typing.Any]]]] = None,
                replication_time: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union[aws_cdk.aws_s3.CfnBucket.ReplicationTimeProperty, typing.Dict[str, typing.Any]]]] = None,
                storage_class: typing.Optional["ReplicationDestinationStorageClass"] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument access_control_translation", value=access_control_translation, expected_type=type_hints["access_control_translation"])
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
            check_type(argname="argument metrics", value=metrics, expected_type=type_hints["metrics"])
            check_type(argname="argument replication_time", value=replication_time, expected_type=type_hints["replication_time"])
            check_type(argname="argument storage_class", value=storage_class, expected_type=type_hints["storage_class"])
        self._values: typing.Dict[str, typing.Any] = {}
        if access_control_translation is not None:
            self._values["access_control_translation"] = access_control_translation
        if account is not None:
            self._values["account"] = account
        if encryption_configuration is not None:
            self._values["encryption_configuration"] = encryption_configuration
        if metrics is not None:
            self._values["metrics"] = metrics
        if replication_time is not None:
            self._values["replication_time"] = replication_time
        if storage_class is not None:
            self._values["storage_class"] = storage_class

    @builtins.property
    def access_control_translation(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, aws_cdk.aws_s3.CfnBucket.AccessControlTranslationProperty]]:
        result = self._values.get("access_control_translation")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, aws_cdk.aws_s3.CfnBucket.AccessControlTranslationProperty]], result)

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, aws_cdk.aws_s3.CfnBucket.EncryptionConfigurationProperty]]:
        result = self._values.get("encryption_configuration")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, aws_cdk.aws_s3.CfnBucket.EncryptionConfigurationProperty]], result)

    @builtins.property
    def metrics(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, aws_cdk.aws_s3.CfnBucket.MetricsProperty]]:
        result = self._values.get("metrics")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, aws_cdk.aws_s3.CfnBucket.MetricsProperty]], result)

    @builtins.property
    def replication_time(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, aws_cdk.aws_s3.CfnBucket.ReplicationTimeProperty]]:
        result = self._values.get("replication_time")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, aws_cdk.aws_s3.CfnBucket.ReplicationTimeProperty]], result)

    @builtins.property
    def storage_class(self) -> typing.Optional["ReplicationDestinationStorageClass"]:
        result = self._values.get("storage_class")
        return typing.cast(typing.Optional["ReplicationDestinationStorageClass"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReplicationDestinationPropertyNoBucket(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-s3-bucketreplication.ReplicationDestinationStorageClass")
class ReplicationDestinationStorageClass(enum.Enum):
    DEEP_ARCHIVE = "DEEP_ARCHIVE"
    GLACIER = "GLACIER"
    INTELLIGENT_TIERING = "INTELLIGENT_TIERING"
    ONEZONE_IA = "ONEZONE_IA"
    OUTPOSTS = "OUTPOSTS"
    REDUCED_REDUNDANCY = "REDUCED_REDUNDANCY"
    STANDARD = "STANDARD"
    STANDARD_IA = "STANDARD_IA"


@jsii.data_type(
    jsii_type="cdk-s3-bucketreplication.ReplicationRulePropertyNoDestination",
    jsii_struct_bases=[],
    name_mapping={
        "delete_marker_replication": "deleteMarkerReplication",
        "filter": "filter",
        "id": "id",
        "prefix": "prefix",
        "priority": "priority",
        "source_selection_criteria": "sourceSelectionCriteria",
        "status": "status",
    },
)
class ReplicationRulePropertyNoDestination:
    def __init__(
        self,
        *,
        delete_marker_replication: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union[aws_cdk.aws_s3.CfnBucket.DeleteMarkerReplicationProperty, typing.Dict[str, typing.Any]]]] = None,
        filter: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union[aws_cdk.aws_s3.CfnBucket.ReplicationRuleFilterProperty, typing.Dict[str, typing.Any]]]] = None,
        id: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        source_selection_criteria: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union[aws_cdk.aws_s3.CfnBucket.SourceSelectionCriteriaProperty, typing.Dict[str, typing.Any]]]] = None,
        status: typing.Optional["ReplicationRuleStatus"] = None,
    ) -> None:
        '''
        :param delete_marker_replication: 
        :param filter: 
        :param id: 
        :param prefix: 
        :param priority: 
        :param source_selection_criteria: 
        :param status: 
        '''
        if __debug__:
            def stub(
                *,
                delete_marker_replication: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union[aws_cdk.aws_s3.CfnBucket.DeleteMarkerReplicationProperty, typing.Dict[str, typing.Any]]]] = None,
                filter: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union[aws_cdk.aws_s3.CfnBucket.ReplicationRuleFilterProperty, typing.Dict[str, typing.Any]]]] = None,
                id: typing.Optional[builtins.str] = None,
                prefix: typing.Optional[builtins.str] = None,
                priority: typing.Optional[jsii.Number] = None,
                source_selection_criteria: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Union[aws_cdk.aws_s3.CfnBucket.SourceSelectionCriteriaProperty, typing.Dict[str, typing.Any]]]] = None,
                status: typing.Optional["ReplicationRuleStatus"] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument delete_marker_replication", value=delete_marker_replication, expected_type=type_hints["delete_marker_replication"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument source_selection_criteria", value=source_selection_criteria, expected_type=type_hints["source_selection_criteria"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[str, typing.Any] = {}
        if delete_marker_replication is not None:
            self._values["delete_marker_replication"] = delete_marker_replication
        if filter is not None:
            self._values["filter"] = filter
        if id is not None:
            self._values["id"] = id
        if prefix is not None:
            self._values["prefix"] = prefix
        if priority is not None:
            self._values["priority"] = priority
        if source_selection_criteria is not None:
            self._values["source_selection_criteria"] = source_selection_criteria
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def delete_marker_replication(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, aws_cdk.aws_s3.CfnBucket.DeleteMarkerReplicationProperty]]:
        result = self._values.get("delete_marker_replication")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, aws_cdk.aws_s3.CfnBucket.DeleteMarkerReplicationProperty]], result)

    @builtins.property
    def filter(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, aws_cdk.aws_s3.CfnBucket.ReplicationRuleFilterProperty]]:
        result = self._values.get("filter")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, aws_cdk.aws_s3.CfnBucket.ReplicationRuleFilterProperty]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def source_selection_criteria(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, aws_cdk.aws_s3.CfnBucket.SourceSelectionCriteriaProperty]]:
        result = self._values.get("source_selection_criteria")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, aws_cdk.aws_s3.CfnBucket.SourceSelectionCriteriaProperty]], result)

    @builtins.property
    def status(self) -> typing.Optional["ReplicationRuleStatus"]:
        result = self._values.get("status")
        return typing.cast(typing.Optional["ReplicationRuleStatus"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReplicationRulePropertyNoDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-s3-bucketreplication.ReplicationRuleStatus")
class ReplicationRuleStatus(enum.Enum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


__all__ = [
    "BucketReplication",
    "BucketReplicationProps",
    "ReplicationDestinationPropertyNoBucket",
    "ReplicationDestinationStorageClass",
    "ReplicationRulePropertyNoDestination",
    "ReplicationRuleStatus",
]

publication.publish()
