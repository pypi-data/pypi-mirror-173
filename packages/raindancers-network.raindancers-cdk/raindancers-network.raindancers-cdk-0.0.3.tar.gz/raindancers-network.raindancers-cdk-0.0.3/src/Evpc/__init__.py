'''
# Raindancers Evpc Construct Library

The raindancers-cdk/raindancers network package contains a constructs that extends the ec2.Vpc construct to provide additional capablitys, particually for using in an enterprise network.

All of the methods that work with ec2.Vpc, work with Evpc.   Refer to [the ec2.Vpc Documentation](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2-readme.html)

```
import { Evpc } from 'raindancers-cdk.raindancers-network';
```

## VPC

Many projects need a Virtual Private Cloud network.  This can be provided by creating an instance of `EVpc` :

```
const shineyEvpc = new Evpc(this, 'EnterpriseVPC');
```

### Using IPAM address Pool for Addressing in Cidr

Creating a vpc that gets its Ip Address allocation from an IPAM pool, requires providing a netmask and ipamPoolId.  Only one of ipamPoolId or cidr is allowed.    The underlying resource that creates a VPC natively consumes IPAM.

```
const shineyEpvc = new Evpc(this, 'EnterpriseVPC', {
	ipamPoolId: 'pool-00000122344',
	netmaskLength: 24
})
```

### Centralised Flow Logs and Athena Querys.

This construct will create a flow log, that is written to a centralised flow log bucket. The construct expects to find the bucket name in they key `flowlogbucket` in cdk.json. (This typically is in the log-archive acount, set up by Control Tower). This requires that the buckets policy allows access. To DISABLE this feature, set the disableFLowLog to `false`.  By default the flow log will aggregate flow logs at a 10minute internal.  To enable aggregation on a 1 minute interval, set the oneMinuteFlowLogs property to true.

The construct will also create a set of Athena querys and glue jobs that will provide an easy way to query the flow logs from within the account that the vpc is created.

```
const shineyEpvc = new Evpc(this, 'EnterpriseVPC', {
	disableFlowlog: false,
	oneMinuteFlowLogs: true
})
```

### Subnets

The construct creates subnets in the same way that the ec2.Vpc construct does.   in order to connect the VPC to a cloudWAN, the construct requires that a subnet group called 'linknets' is created.  This is where the attachments for cloudwan will be created.

```
const shiney = new Evpc(this, 'Shineyvpc', {
	r53InternalZoneName: 'thing.domain.com'
	ipamPoolId: 'ip-pool-id',
	subnetConfiguration: [
		{
			name: 'linknet',
			subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
			cidrMask: 28
		},
	]
	}
)
```

### Attaching a VPC to cloud wan.

To attach a vpc to a cloudwan, use the attachToCloudWan method, for example to connect to a core network 'AcmeCore' and segment 'AppsProd';  The attachments to cloudwan will be made in the linknets subnets

```
const shineyVpc = new Evpc: Evpc;
shineyVpc.attachToCloudWan('AcmeCore', 'AppsProd')
```

This method returns the attachmentId, which is used in the routing methods.

## Attaching a VPC to a TransitGateway in Appliance Mode.

(very beta and potentially buggy)
TODO: Write doc's

### Adding Routes to Cloudwan attached VPC's

A number of convience methods are provided to add routes to the cloudwan; For example to add a default route (0/0) in all privatesubnets

```
shineyVpc.addRouteForPrivateSubnetstoCloudwan('0.0.0.0/0', attachmentId)
```

Similar method exisits for PublicSubnets, TransitGateways Instances and Firewalls.

### Internal Route53 Zones

A internal Route53 Zone can be created and associated with the Vpc, by specifying the r53InternalZoneName property

```
const shineyEpvc = new Evpc(this, 'EnterpriseVPC', {
	r53InternalZoneName: 'internal.somedomain.cloud',
})
```

## DNS Methods

To do.
associateVPCZonewithCentralVPC
associateSharedRoute53ResolverRules

# IPAM

This package contains constructs for integrating with **Amazon IP Address Manager**.  While the IPAM Service is GA and provides a very useful service, only a handful of services natively support ingesting a IPAM allocated address ( ie, VPC ).

For futher infomation on Amazon IPAM, see the [IPAM Documentation](https://docs.aws.amazon.com/vpc/latest/ipam/getting-started-ipam.html)

### Using IPAM for IPsec VPN tunnel addresses

The Cidr ranges for IPSec VPN Tunnels must comply to several constraints.

* they must be a /30
* they must be subnets of 169.254.0.0/16
* they must not conflict with the reserved subnets ( see docs above )

The following example demonstrates how the constructs can be used to create an address Pool and suitable allocations, that met these criteria

```

const tunnelIPAMPool = new kapua_ipam.IpsecTunnelPool(this, 'ipampool', {
	ipamScopeId: 'ipam-scope-00112233445566778',
	cidr: '169.254.100.0/27',
	description: 'Addressing for IPSec Tunnels between ap-southeast-2 and on prem',
	name: 'ToOnPremVPNTunnels'
})


var assignedCidrs: string[] = []

const tunnelAllocation = new GetTunnelAddressPair(this, `${name}tunneladdress`,{
	ipamPoolId: tunnelIPAMPool.attrIpamPoolId,
	name: name
})

assignedCidrs = tunnelAllocation.assignedCidrPair

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

import aws_cdk
import aws_cdk.aws_dynamodb
import aws_cdk.aws_ec2
import aws_cdk.aws_networkmanager
import aws_cdk.aws_route53
import aws_cdk.aws_sns
import aws_cdk.custom_resources
import constructs


@jsii.enum(jsii_type="raindancers-network.AssociationMethod")
class AssociationMethod(enum.Enum):
    '''(experimental) Association Methods.

    :stability: experimental
    '''

    CONSTANT = "CONSTANT"
    '''
    :stability: experimental
    '''
    TAG = "TAG"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="raindancers-network.AttachmentCondition")
class AttachmentCondition(enum.Enum):
    '''(experimental) Attachment Conditions.

    :stability: experimental
    '''

    ANY = "ANY"
    '''
    :stability: experimental
    '''
    RESOURCE_ID = "RESOURCE_ID"
    '''
    :stability: experimental
    '''
    ACCOUNT_ID = "ACCOUNT_ID"
    '''
    :stability: experimental
    '''
    REGION = "REGION"
    '''
    :stability: experimental
    '''
    ATTACHMENT_TYPE = "ATTACHMENT_TYPE"
    '''
    :stability: experimental
    '''
    TAG_EXISTS = "TAG_EXISTS"
    '''
    :stability: experimental
    '''
    TAG_VALUE = "TAG_VALUE"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="raindancers-network.AttachmentConditions",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "key": "key",
        "operator": "operator",
        "value": "value",
    },
)
class AttachmentConditions:
    def __init__(
        self,
        *,
        type: AttachmentCondition,
        key: typing.Optional[builtins.str] = None,
        operator: typing.Optional["Operators"] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) an attachmentconditions.

        :param type: 
        :param key: 
        :param operator: 
        :param value: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AttachmentConditions.__init__)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[str, typing.Any] = {
            "type": type,
        }
        if key is not None:
            self._values["key"] = key
        if operator is not None:
            self._values["operator"] = operator
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def type(self) -> AttachmentCondition:
        '''
        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(AttachmentCondition, result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operator(self) -> typing.Optional["Operators"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("operator")
        return typing.cast(typing.Optional["Operators"], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AttachmentConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.AttachmentPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "conditions": "conditions",
        "rule_number": "ruleNumber",
        "condition_logic": "conditionLogic",
        "description": "description",
    },
)
class AttachmentPolicy:
    def __init__(
        self,
        *,
        action: typing.Union["AttachmentPolicyAction", typing.Dict[str, typing.Any]],
        conditions: typing.Sequence[AttachmentCondition],
        rule_number: jsii.Number,
        condition_logic: typing.Optional["ConditionLogic"] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) an attachment policy.

        :param action: 
        :param conditions: 
        :param rule_number: 
        :param condition_logic: 
        :param description: 

        :stability: experimental
        '''
        if isinstance(action, dict):
            action = AttachmentPolicyAction(**action)
        if __debug__:
            type_hints = typing.get_type_hints(AttachmentPolicy.__init__)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument rule_number", value=rule_number, expected_type=type_hints["rule_number"])
            check_type(argname="argument condition_logic", value=condition_logic, expected_type=type_hints["condition_logic"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[str, typing.Any] = {
            "action": action,
            "conditions": conditions,
            "rule_number": rule_number,
        }
        if condition_logic is not None:
            self._values["condition_logic"] = condition_logic
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def action(self) -> "AttachmentPolicyAction":
        '''
        :stability: experimental
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast("AttachmentPolicyAction", result)

    @builtins.property
    def conditions(self) -> typing.List[AttachmentCondition]:
        '''
        :stability: experimental
        '''
        result = self._values.get("conditions")
        assert result is not None, "Required property 'conditions' is missing"
        return typing.cast(typing.List[AttachmentCondition], result)

    @builtins.property
    def rule_number(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        result = self._values.get("rule_number")
        assert result is not None, "Required property 'rule_number' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def condition_logic(self) -> typing.Optional["ConditionLogic"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("condition_logic")
        return typing.cast(typing.Optional["ConditionLogic"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AttachmentPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.AttachmentPolicyAction",
    jsii_struct_bases=[],
    name_mapping={"association_method": "associationMethod", "segment": "segment"},
)
class AttachmentPolicyAction:
    def __init__(
        self,
        *,
        association_method: AssociationMethod,
        segment: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Attachment Policy Action.

        :param association_method: (experimental) The Assocation Method.
        :param segment: (experimental) The Segment this applies to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AttachmentPolicyAction.__init__)
            check_type(argname="argument association_method", value=association_method, expected_type=type_hints["association_method"])
            check_type(argname="argument segment", value=segment, expected_type=type_hints["segment"])
        self._values: typing.Dict[str, typing.Any] = {
            "association_method": association_method,
        }
        if segment is not None:
            self._values["segment"] = segment

    @builtins.property
    def association_method(self) -> AssociationMethod:
        '''(experimental) The Assocation Method.

        :stability: experimental
        '''
        result = self._values.get("association_method")
        assert result is not None, "Required property 'association_method' is missing"
        return typing.cast(AssociationMethod, result)

    @builtins.property
    def segment(self) -> typing.Optional[builtins.str]:
        '''(experimental) The Segment this applies to.

        :stability: experimental
        '''
        result = self._values.get("segment")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AttachmentPolicyAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="raindancers-network.ConditionLogic")
class ConditionLogic(enum.Enum):
    '''(experimental) Conditon Logic.

    :stability: experimental
    '''

    AND = "AND"
    '''
    :stability: experimental
    '''
    OR = "OR"
    '''
    :stability: experimental
    '''


class CoreNetwork(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.CoreNetwork",
):
    '''(experimental) Create a CoreNework for a Cloudwan.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        asn_ranges: typing.Sequence[builtins.str],
        core_name: builtins.str,
        edge_locations: typing.Sequence[typing.Mapping[typing.Any, typing.Any]],
        global_network: aws_cdk.aws_networkmanager.CfnGlobalNetwork,
        policy_description: builtins.str,
        inside_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpn_ecmp_support: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param asn_ranges: (experimental) a list of of asn's that can be used.
        :param core_name: (experimental) core name.
        :param edge_locations: (experimental) list of edgeLocaitons.
        :param global_network: (experimental) Which Global Network.
        :param policy_description: (experimental) a decription for the policy Document.
        :param inside_cidr_blocks: (experimental) List of InsideCidr Blocks.
        :param vpn_ecmp_support: (experimental) support VpnECmp.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CoreNetwork.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CoreNetworkProps(
            asn_ranges=asn_ranges,
            core_name=core_name,
            edge_locations=edge_locations,
            global_network=global_network,
            policy_description=policy_description,
            inside_cidr_blocks=inside_cidr_blocks,
            vpn_ecmp_support=vpn_ecmp_support,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addSegment")
    def add_segment(
        self,
        *,
        name: builtins.str,
        allow_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        deny_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        edge_locations: typing.Optional[typing.Sequence[typing.Mapping[typing.Any, typing.Any]]] = None,
        isolate_attachments: typing.Optional[builtins.bool] = None,
        require_attachment_acceptance: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Add a segment to the core network.

        :param name: (experimental) Name of the Segment.
        :param allow_filter: (experimental) A list of denys.
        :param deny_filter: (experimental) a List of denys.
        :param description: (experimental) A description of the of the segement.
        :param edge_locations: (experimental) A list of edge locations where the segement will be avaialble. Not that the locations must also be included in the core network edge ( CNE )
        :param isolate_attachments: (experimental) Set true if attached VPCS are isolated from each other.
        :param require_attachment_acceptance: (experimental) Set true if the attachment needs approval for connection. Currently not supported and requires an automation step

        :stability: experimental
        '''
        props = Segment(
            name=name,
            allow_filter=allow_filter,
            deny_filter=deny_filter,
            description=description,
            edge_locations=edge_locations,
            isolate_attachments=isolate_attachments,
            require_attachment_acceptance=require_attachment_acceptance,
        )

        return typing.cast(None, jsii.invoke(self, "addSegment", [props]))

    @jsii.member(jsii_name="share")
    def share(
        self,
        *,
        allow_external_principals: builtins.bool,
        principals: typing.Sequence[builtins.str],
        tags: typing.Optional[typing.Sequence[aws_cdk.Tag]] = None,
    ) -> None:
        '''(experimental) Create a CoreNetwork Sharing.

        :param allow_external_principals: 
        :param principals: 
        :param tags: 

        :stability: experimental
        '''
        props = CoreNetworkShare(
            allow_external_principals=allow_external_principals,
            principals=principals,
            tags=tags,
        )

        return typing.cast(None, jsii.invoke(self, "share", [props]))

    @jsii.member(jsii_name="updatePolicy")
    def update_policy(self) -> None:
        '''(experimental) Update the corewan policy after actions, segments are added.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "updatePolicy", []))

    @builtins.property
    @jsii.member(jsii_name="cfnCoreNetwork")
    def cfn_core_network(self) -> aws_cdk.aws_networkmanager.CfnCoreNetwork:
        '''(experimental) The corenetwork object.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_networkmanager.CfnCoreNetwork, jsii.get(self, "cfnCoreNetwork"))

    @builtins.property
    @jsii.member(jsii_name="coreName")
    def core_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "coreName"))

    @builtins.property
    @jsii.member(jsii_name="policyTable")
    def policy_table(self) -> aws_cdk.aws_dynamodb.Table:
        '''(experimental) THe dynamo table holding the policy.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_dynamodb.Table, jsii.get(self, "policyTable"))

    @builtins.property
    @jsii.member(jsii_name="policyTableName")
    def policy_table_name(self) -> builtins.str:
        '''(experimental) Name of the Dynamo Table holding the policy.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "policyTableName"))

    @builtins.property
    @jsii.member(jsii_name="policyTableServiceToken")
    def policy_table_service_token(self) -> builtins.str:
        '''(experimental) The policyTable Lamba's Service Token.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "policyTableServiceToken"))

    @builtins.property
    @jsii.member(jsii_name="updateProviderToken")
    def update_provider_token(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "updateProviderToken"))

    @update_provider_token.setter
    def update_provider_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(CoreNetwork, "update_provider_token").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updateProviderToken", value)


@jsii.data_type(
    jsii_type="raindancers-network.CoreNetworkProps",
    jsii_struct_bases=[],
    name_mapping={
        "asn_ranges": "asnRanges",
        "core_name": "coreName",
        "edge_locations": "edgeLocations",
        "global_network": "globalNetwork",
        "policy_description": "policyDescription",
        "inside_cidr_blocks": "insideCidrBlocks",
        "vpn_ecmp_support": "vpnEcmpSupport",
    },
)
class CoreNetworkProps:
    def __init__(
        self,
        *,
        asn_ranges: typing.Sequence[builtins.str],
        core_name: builtins.str,
        edge_locations: typing.Sequence[typing.Mapping[typing.Any, typing.Any]],
        global_network: aws_cdk.aws_networkmanager.CfnGlobalNetwork,
        policy_description: builtins.str,
        inside_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpn_ecmp_support: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) CoreNetwork Properties.

        :param asn_ranges: (experimental) a list of of asn's that can be used.
        :param core_name: (experimental) core name.
        :param edge_locations: (experimental) list of edgeLocaitons.
        :param global_network: (experimental) Which Global Network.
        :param policy_description: (experimental) a decription for the policy Document.
        :param inside_cidr_blocks: (experimental) List of InsideCidr Blocks.
        :param vpn_ecmp_support: (experimental) support VpnECmp.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CoreNetworkProps.__init__)
            check_type(argname="argument asn_ranges", value=asn_ranges, expected_type=type_hints["asn_ranges"])
            check_type(argname="argument core_name", value=core_name, expected_type=type_hints["core_name"])
            check_type(argname="argument edge_locations", value=edge_locations, expected_type=type_hints["edge_locations"])
            check_type(argname="argument global_network", value=global_network, expected_type=type_hints["global_network"])
            check_type(argname="argument policy_description", value=policy_description, expected_type=type_hints["policy_description"])
            check_type(argname="argument inside_cidr_blocks", value=inside_cidr_blocks, expected_type=type_hints["inside_cidr_blocks"])
            check_type(argname="argument vpn_ecmp_support", value=vpn_ecmp_support, expected_type=type_hints["vpn_ecmp_support"])
        self._values: typing.Dict[str, typing.Any] = {
            "asn_ranges": asn_ranges,
            "core_name": core_name,
            "edge_locations": edge_locations,
            "global_network": global_network,
            "policy_description": policy_description,
        }
        if inside_cidr_blocks is not None:
            self._values["inside_cidr_blocks"] = inside_cidr_blocks
        if vpn_ecmp_support is not None:
            self._values["vpn_ecmp_support"] = vpn_ecmp_support

    @builtins.property
    def asn_ranges(self) -> typing.List[builtins.str]:
        '''(experimental) a list of of asn's that can be used.

        :stability: experimental
        '''
        result = self._values.get("asn_ranges")
        assert result is not None, "Required property 'asn_ranges' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def core_name(self) -> builtins.str:
        '''(experimental) core name.

        :stability: experimental
        '''
        result = self._values.get("core_name")
        assert result is not None, "Required property 'core_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def edge_locations(self) -> typing.List[typing.Mapping[typing.Any, typing.Any]]:
        '''(experimental) list of edgeLocaitons.

        :stability: experimental
        '''
        result = self._values.get("edge_locations")
        assert result is not None, "Required property 'edge_locations' is missing"
        return typing.cast(typing.List[typing.Mapping[typing.Any, typing.Any]], result)

    @builtins.property
    def global_network(self) -> aws_cdk.aws_networkmanager.CfnGlobalNetwork:
        '''(experimental) Which Global Network.

        :stability: experimental
        '''
        result = self._values.get("global_network")
        assert result is not None, "Required property 'global_network' is missing"
        return typing.cast(aws_cdk.aws_networkmanager.CfnGlobalNetwork, result)

    @builtins.property
    def policy_description(self) -> builtins.str:
        '''(experimental) a decription for the policy Document.

        :stability: experimental
        '''
        result = self._values.get("policy_description")
        assert result is not None, "Required property 'policy_description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def inside_cidr_blocks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of InsideCidr Blocks.

        :stability: experimental
        '''
        result = self._values.get("inside_cidr_blocks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vpn_ecmp_support(self) -> typing.Optional[builtins.bool]:
        '''(experimental) support VpnECmp.

        :stability: experimental
        '''
        result = self._values.get("vpn_ecmp_support")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CoreNetworkProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.CoreNetworkShare",
    jsii_struct_bases=[],
    name_mapping={
        "allow_external_principals": "allowExternalPrincipals",
        "principals": "principals",
        "tags": "tags",
    },
)
class CoreNetworkShare:
    def __init__(
        self,
        *,
        allow_external_principals: builtins.bool,
        principals: typing.Sequence[builtins.str],
        tags: typing.Optional[typing.Sequence[aws_cdk.Tag]] = None,
    ) -> None:
        '''(experimental) CoreNetworkShare.

        :param allow_external_principals: 
        :param principals: 
        :param tags: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CoreNetworkShare.__init__)
            check_type(argname="argument allow_external_principals", value=allow_external_principals, expected_type=type_hints["allow_external_principals"])
            check_type(argname="argument principals", value=principals, expected_type=type_hints["principals"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[str, typing.Any] = {
            "allow_external_principals": allow_external_principals,
            "principals": principals,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def allow_external_principals(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        result = self._values.get("allow_external_principals")
        assert result is not None, "Required property 'allow_external_principals' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def principals(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("principals")
        assert result is not None, "Required property 'principals' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.Tag]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[aws_cdk.Tag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CoreNetworkShare(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Evpc(
    aws_cdk.aws_ec2.Vpc,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.Evpc",
):
    '''(experimental) Extends the ec2.Vpc construct to provide additional functionality - support for using AWS IPAM - methods for integration - Flow logs and Athena Querys - Create and share 53 zones.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        attach_to_core_network_segment: typing.Optional[builtins.str] = None,
        central_resolving_vpc: typing.Optional[builtins.bool] = None,
        disable_flowlog: typing.Optional[builtins.bool] = None,
        internet_gateway: typing.Optional[builtins.bool] = None,
        ipam_pool_id: typing.Optional[builtins.str] = None,
        netmask_length: typing.Optional[jsii.Number] = None,
        one_minute_flow_logs: typing.Optional[builtins.bool] = None,
        r53_internal_zone_name: typing.Optional[builtins.str] = None,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cidr: typing.Optional[builtins.str] = None,
        default_instance_tenancy: typing.Optional[aws_cdk.aws_ec2.DefaultInstanceTenancy] = None,
        enable_dns_hostnames: typing.Optional[builtins.bool] = None,
        enable_dns_support: typing.Optional[builtins.bool] = None,
        flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[aws_cdk.aws_ec2.FlowLogOptions, typing.Dict[str, typing.Any]]]] = None,
        gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[aws_cdk.aws_ec2.GatewayVpcEndpointOptions, typing.Dict[str, typing.Any]]]] = None,
        max_azs: typing.Optional[jsii.Number] = None,
        nat_gateway_provider: typing.Optional[aws_cdk.aws_ec2.NatProvider] = None,
        nat_gateways: typing.Optional[jsii.Number] = None,
        nat_gateway_subnets: typing.Optional[typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]]] = None,
        subnet_configuration: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_ec2.SubnetConfiguration, typing.Dict[str, typing.Any]]]] = None,
        vpc_name: typing.Optional[builtins.str] = None,
        vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[aws_cdk.aws_ec2.VpnConnectionOptions, typing.Dict[str, typing.Any]]]] = None,
        vpn_gateway: typing.Optional[builtins.bool] = None,
        vpn_gateway_asn: typing.Optional[jsii.Number] = None,
        vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param attach_to_core_network_segment: (experimental) the cloudwan core network segment name that this vpc will be attached to.
        :param central_resolving_vpc: (experimental) Set true if this is the central resolving Vpc.
        :param disable_flowlog: (experimental) Set true to disable centralised Flow Logs.
        :param internet_gateway: (experimental) An Internet Gateway will only be created if true.
        :param ipam_pool_id: (experimental) the ipam pool id that the Vpc's allocation will get created in.
        :param netmask_length: (experimental) a netmask value that is in the range 16 to 28.
        :param one_minute_flow_logs: (experimental) Set true for 1 minute aggregation on flow logs. (default is 10 minutes )
        :param r53_internal_zone_name: (experimental) Name of an internal Route53 Zone that is associated with this voc.
        :param availability_zones: Availability zones this VPC spans. Specify this option only if you do not specify ``maxAzs``. Default: - a subset of AZs of the stack
        :param cidr: The CIDR range to use for the VPC, e.g. '10.0.0.0/16'. Should be a minimum of /28 and maximum size of /16. The range will be split across all subnets per Availability Zone. Default: Vpc.DEFAULT_CIDR_RANGE
        :param default_instance_tenancy: The default tenancy of instances launched into the VPC. By setting this to dedicated tenancy, instances will be launched on hardware dedicated to a single AWS customer, unless specifically specified at instance launch time. Please note, not all instance types are usable with Dedicated tenancy. Default: DefaultInstanceTenancy.Default (shared) tenancy
        :param enable_dns_hostnames: Indicates whether the instances launched in the VPC get public DNS hostnames. If this attribute is true, instances in the VPC get public DNS hostnames, but only if the enableDnsSupport attribute is also set to true. Default: true
        :param enable_dns_support: Indicates whether the DNS resolution is supported for the VPC. If this attribute is false, the Amazon-provided DNS server in the VPC that resolves public DNS hostnames to IP addresses is not enabled. If this attribute is true, queries to the Amazon provided DNS server at the 169.254.169.253 IP address, or the reserved IP address at the base of the VPC IPv4 network range plus two will succeed. Default: true
        :param flow_logs: Flow logs to add to this VPC. Default: - No flow logs.
        :param gateway_endpoints: Gateway endpoints to add to this VPC. Default: - None.
        :param max_azs: Define the maximum number of AZs to use in this region. If the region has more AZs than you want to use (for example, because of EIP limits), pick a lower number here. The AZs will be sorted and picked from the start of the list. If you pick a higher number than the number of AZs in the region, all AZs in the region will be selected. To use "all AZs" available to your account, use a high number (such as 99). Be aware that environment-agnostic stacks will be created with access to only 2 AZs, so to use more than 2 AZs, be sure to specify the account and region on your stack. Specify this option only if you do not specify ``availabilityZones``. Default: 3
        :param nat_gateway_provider: What type of NAT provider to use. Select between NAT gateways or NAT instances. NAT gateways may not be available in all AWS regions. Default: NatProvider.gateway()
        :param nat_gateways: The number of NAT Gateways/Instances to create. The type of NAT gateway or instance will be determined by the ``natGatewayProvider`` parameter. You can set this number lower than the number of Availability Zones in your VPC in order to save on NAT cost. Be aware you may be charged for cross-AZ data traffic instead. Default: - One NAT gateway/instance per Availability Zone
        :param nat_gateway_subnets: Configures the subnets which will have NAT Gateways/Instances. You can pick a specific group of subnets by specifying the group name; the picked subnets must be public subnets. Only necessary if you have more than one public subnet group. Default: - All public subnets.
        :param subnet_configuration: Configure the subnets to build for each AZ. Each entry in this list configures a Subnet Group; each group will contain a subnet for each Availability Zone. For example, if you want 1 public subnet, 1 private subnet, and 1 isolated subnet in each AZ provide the following:: new ec2.Vpc(this, 'VPC', { subnetConfiguration: [ { cidrMask: 24, name: 'ingress', subnetType: ec2.SubnetType.PUBLIC, }, { cidrMask: 24, name: 'application', subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS, }, { cidrMask: 28, name: 'rds', subnetType: ec2.SubnetType.PRIVATE_ISOLATED, } ] }); Default: - The VPC CIDR will be evenly divided between 1 public and 1 private subnet per AZ.
        :param vpc_name: The VPC name. Since the VPC resource doesn't support providing a physical name, the value provided here will be recorded in the ``Name`` tag Default: this.node.path
        :param vpn_connections: VPN connections to this VPC. Default: - No connections.
        :param vpn_gateway: Indicates whether a VPN gateway should be created and attached to this VPC. Default: - true when vpnGatewayAsn or vpnConnections is specified
        :param vpn_gateway_asn: The private Autonomous System Number (ASN) for the VPN gateway. Default: - Amazon default ASN.
        :param vpn_route_propagation: Where to propagate VPN routes. Default: - On the route tables associated with private subnets. If no private subnets exists, isolated subnets are used. If no isolated subnets exists, public subnets are used.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Evpc.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EvpcProps(
            attach_to_core_network_segment=attach_to_core_network_segment,
            central_resolving_vpc=central_resolving_vpc,
            disable_flowlog=disable_flowlog,
            internet_gateway=internet_gateway,
            ipam_pool_id=ipam_pool_id,
            netmask_length=netmask_length,
            one_minute_flow_logs=one_minute_flow_logs,
            r53_internal_zone_name=r53_internal_zone_name,
            availability_zones=availability_zones,
            cidr=cidr,
            default_instance_tenancy=default_instance_tenancy,
            enable_dns_hostnames=enable_dns_hostnames,
            enable_dns_support=enable_dns_support,
            flow_logs=flow_logs,
            gateway_endpoints=gateway_endpoints,
            max_azs=max_azs,
            nat_gateway_provider=nat_gateway_provider,
            nat_gateways=nat_gateways,
            nat_gateway_subnets=nat_gateway_subnets,
            subnet_configuration=subnet_configuration,
            vpc_name=vpc_name,
            vpn_connections=vpn_connections,
            vpn_gateway=vpn_gateway,
            vpn_gateway_asn=vpn_gateway_asn,
            vpn_route_propagation=vpn_route_propagation,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addRouteForPrivateSubnetstoCloudWan")
    def add_route_for_private_subnetsto_cloud_wan(
        self,
        destination_cidr: builtins.str,
        core_network_id: builtins.str,
    ) -> None:
        '''(experimental) Add a route to routing tables attached to the private subnets.

        :param destination_cidr: cidr eg, 0.0.0.0/0.
        :param core_network_id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Evpc.add_route_for_private_subnetsto_cloud_wan)
            check_type(argname="argument destination_cidr", value=destination_cidr, expected_type=type_hints["destination_cidr"])
            check_type(argname="argument core_network_id", value=core_network_id, expected_type=type_hints["core_network_id"])
        return typing.cast(None, jsii.invoke(self, "addRouteForPrivateSubnetstoCloudWan", [destination_cidr, core_network_id]))

    @jsii.member(jsii_name="addRouteForPrivateSubnetstoinstance")
    def add_route_for_private_subnetstoinstance(
        self,
        destination_cidr: builtins.str,
        instance_id: builtins.str,
    ) -> None:
        '''(experimental) Add routes in private Subnets to a instance.

        Use this for routing to a network appliance.

        :param destination_cidr: -
        :param instance_id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Evpc.add_route_for_private_subnetstoinstance)
            check_type(argname="argument destination_cidr", value=destination_cidr, expected_type=type_hints["destination_cidr"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
        return typing.cast(None, jsii.invoke(self, "addRouteForPrivateSubnetstoinstance", [destination_cidr, instance_id]))

    @jsii.member(jsii_name="addRouteForPrivateSubnetstoTransitGateway")
    def add_route_for_private_subnetsto_transit_gateway(
        self,
        destination_cidr: builtins.str,
        transit_gateway_id: builtins.str,
    ) -> None:
        '''(experimental) Add routes for Private Subnets to a Transit Gateway.

        :param destination_cidr: -
        :param transit_gateway_id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Evpc.add_route_for_private_subnetsto_transit_gateway)
            check_type(argname="argument destination_cidr", value=destination_cidr, expected_type=type_hints["destination_cidr"])
            check_type(argname="argument transit_gateway_id", value=transit_gateway_id, expected_type=type_hints["transit_gateway_id"])
        return typing.cast(None, jsii.invoke(self, "addRouteForPrivateSubnetstoTransitGateway", [destination_cidr, transit_gateway_id]))

    @jsii.member(jsii_name="addRouteForPublicSubnetstoCloudWan")
    def add_route_for_public_subnetsto_cloud_wan(
        self,
        destination_cidr: builtins.str,
        core_network_id: builtins.str,
    ) -> None:
        '''(experimental) Add routes to routing tables associated with publicSubnets to Cloudwan.

        :param destination_cidr: -
        :param core_network_id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Evpc.add_route_for_public_subnetsto_cloud_wan)
            check_type(argname="argument destination_cidr", value=destination_cidr, expected_type=type_hints["destination_cidr"])
            check_type(argname="argument core_network_id", value=core_network_id, expected_type=type_hints["core_network_id"])
        return typing.cast(None, jsii.invoke(self, "addRouteForPublicSubnetstoCloudWan", [destination_cidr, core_network_id]))

    @jsii.member(jsii_name="addRoutetoFirewall")
    def add_routeto_firewall(
        self,
        destination_cidr: builtins.str,
        subnetgroup: builtins.str,
        fw_arn: builtins.str,
    ) -> None:
        '''(experimental) Add routes to point at Network Firewalls, for specific subnetGroups.

        this will place routes on a per AZ basis

        :param destination_cidr: -
        :param subnetgroup: -
        :param fw_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Evpc.add_routeto_firewall)
            check_type(argname="argument destination_cidr", value=destination_cidr, expected_type=type_hints["destination_cidr"])
            check_type(argname="argument subnetgroup", value=subnetgroup, expected_type=type_hints["subnetgroup"])
            check_type(argname="argument fw_arn", value=fw_arn, expected_type=type_hints["fw_arn"])
        return typing.cast(None, jsii.invoke(self, "addRoutetoFirewall", [destination_cidr, subnetgroup, fw_arn]))

    @jsii.member(jsii_name="associateSharedRoute53ResolverRules")
    def associate_shared_route53_resolver_rules(
        self,
        owner: builtins.str,
        updatetopic: typing.Optional[aws_cdk.aws_sns.Topic] = None,
    ) -> None:
        '''(experimental) Associate any rules shared to this vpc.

        :param owner: -
        :param updatetopic: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Evpc.associate_shared_route53_resolver_rules)
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument updatetopic", value=updatetopic, expected_type=type_hints["updatetopic"])
        return typing.cast(None, jsii.invoke(self, "associateSharedRoute53ResolverRules", [owner, updatetopic]))

    @jsii.member(jsii_name="associateVPCZonewithCentralVPC")
    def associate_vpc_zonewith_central_vpc(self) -> None:
        '''(experimental) Associate the internal R53 Zone with the Central VPC, for Org wide resolution.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "associateVPCZonewithCentralVPC", []))

    @jsii.member(jsii_name="attachToCloudWan")
    def attach_to_cloud_wan(
        self,
        core_network_name: builtins.str,
        segment: builtins.str,
    ) -> builtins.str:
        '''(experimental) Attach the VPC to a cloud wan segment.

        :param core_network_name: -
        :param segment: -

        :return: transport attachment id

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Evpc.attach_to_cloud_wan)
            check_type(argname="argument core_network_name", value=core_network_name, expected_type=type_hints["core_network_name"])
            check_type(argname="argument segment", value=segment, expected_type=type_hints["segment"])
        return typing.cast(builtins.str, jsii.invoke(self, "attachToCloudWan", [core_network_name, segment]))

    @jsii.member(jsii_name="attachVpcToTGApplianceMode")
    def attach_vpc_to_tg_appliance_mode(
        self,
        transit_gateway: aws_cdk.aws_ec2.CfnTransitGateway,
        cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> builtins.str:
        '''(experimental) Attach a VPC to a Transit Gateway in Appliance mode.

        Primarly used when the VPC is being used as a centralised egress with firewalls
        A workaround to the problem of their not being support for Appliance mode connections to cloudwan

        :param transit_gateway: -
        :param cidrs: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Evpc.attach_vpc_to_tg_appliance_mode)
            check_type(argname="argument transit_gateway", value=transit_gateway, expected_type=type_hints["transit_gateway"])
            check_type(argname="argument cidrs", value=cidrs, expected_type=type_hints["cidrs"])
        return typing.cast(builtins.str, jsii.invoke(self, "attachVpcToTGApplianceMode", [transit_gateway, cidrs]))

    @jsii.member(jsii_name="createConnectAttachment")
    def create_connect_attachment(
        self,
        core_network_id: builtins.str,
        transport_attachment_id: builtins.str,
    ) -> builtins.str:
        '''(experimental) Create a connect Attachment to Cloudwan for Appliances.

        :param core_network_id: -
        :param transport_attachment_id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Evpc.create_connect_attachment)
            check_type(argname="argument core_network_id", value=core_network_id, expected_type=type_hints["core_network_id"])
            check_type(argname="argument transport_attachment_id", value=transport_attachment_id, expected_type=type_hints["transport_attachment_id"])
        return typing.cast(builtins.str, jsii.invoke(self, "createConnectAttachment", [core_network_id, transport_attachment_id]))

    @builtins.property
    @jsii.member(jsii_name="lookUpProvider")
    def look_up_provider(self) -> aws_cdk.custom_resources.Provider:
        '''(experimental) Custom resource provider for looking up Cloudwan.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.custom_resources.Provider, jsii.get(self, "lookUpProvider"))

    @builtins.property
    @jsii.member(jsii_name="centralResolvingVpc")
    def central_resolving_vpc(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If this is a private zone.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "centralResolvingVpc"))

    @builtins.property
    @jsii.member(jsii_name="ipamAllocationId")
    def ipam_allocation_id(self) -> typing.Optional[aws_cdk.aws_ec2.CfnIPAMAllocation]:
        '''(experimental) the Ipam Allocation provider for this vpc.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.CfnIPAMAllocation], jsii.get(self, "ipamAllocationId"))

    @builtins.property
    @jsii.member(jsii_name="linknetSubnetIds")
    def linknet_subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) list of subnetIds that are used for connecting to the Cloudwan.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "linknetSubnetIds"))

    @builtins.property
    @jsii.member(jsii_name="privateR53Zone")
    def private_r53_zone(self) -> typing.Optional[aws_cdk.aws_route53.HostedZone]:
        '''(experimental) Private Zone.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_route53.HostedZone], jsii.get(self, "privateR53Zone"))

    @builtins.property
    @jsii.member(jsii_name="privateR53ZoneId")
    def private_r53_zone_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Private Zone Id.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateR53ZoneId"))


@jsii.data_type(
    jsii_type="raindancers-network.EvpcProps",
    jsii_struct_bases=[aws_cdk.aws_ec2.VpcProps],
    name_mapping={
        "availability_zones": "availabilityZones",
        "cidr": "cidr",
        "default_instance_tenancy": "defaultInstanceTenancy",
        "enable_dns_hostnames": "enableDnsHostnames",
        "enable_dns_support": "enableDnsSupport",
        "flow_logs": "flowLogs",
        "gateway_endpoints": "gatewayEndpoints",
        "max_azs": "maxAzs",
        "nat_gateway_provider": "natGatewayProvider",
        "nat_gateways": "natGateways",
        "nat_gateway_subnets": "natGatewaySubnets",
        "subnet_configuration": "subnetConfiguration",
        "vpc_name": "vpcName",
        "vpn_connections": "vpnConnections",
        "vpn_gateway": "vpnGateway",
        "vpn_gateway_asn": "vpnGatewayAsn",
        "vpn_route_propagation": "vpnRoutePropagation",
        "attach_to_core_network_segment": "attachToCoreNetworkSegment",
        "central_resolving_vpc": "centralResolvingVpc",
        "disable_flowlog": "disableFlowlog",
        "internet_gateway": "internetGateway",
        "ipam_pool_id": "ipamPoolId",
        "netmask_length": "netmaskLength",
        "one_minute_flow_logs": "oneMinuteFlowLogs",
        "r53_internal_zone_name": "r53InternalZoneName",
    },
)
class EvpcProps(aws_cdk.aws_ec2.VpcProps):
    def __init__(
        self,
        *,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cidr: typing.Optional[builtins.str] = None,
        default_instance_tenancy: typing.Optional[aws_cdk.aws_ec2.DefaultInstanceTenancy] = None,
        enable_dns_hostnames: typing.Optional[builtins.bool] = None,
        enable_dns_support: typing.Optional[builtins.bool] = None,
        flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[aws_cdk.aws_ec2.FlowLogOptions, typing.Dict[str, typing.Any]]]] = None,
        gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[aws_cdk.aws_ec2.GatewayVpcEndpointOptions, typing.Dict[str, typing.Any]]]] = None,
        max_azs: typing.Optional[jsii.Number] = None,
        nat_gateway_provider: typing.Optional[aws_cdk.aws_ec2.NatProvider] = None,
        nat_gateways: typing.Optional[jsii.Number] = None,
        nat_gateway_subnets: typing.Optional[typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]]] = None,
        subnet_configuration: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_ec2.SubnetConfiguration, typing.Dict[str, typing.Any]]]] = None,
        vpc_name: typing.Optional[builtins.str] = None,
        vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[aws_cdk.aws_ec2.VpnConnectionOptions, typing.Dict[str, typing.Any]]]] = None,
        vpn_gateway: typing.Optional[builtins.bool] = None,
        vpn_gateway_asn: typing.Optional[jsii.Number] = None,
        vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]]]] = None,
        attach_to_core_network_segment: typing.Optional[builtins.str] = None,
        central_resolving_vpc: typing.Optional[builtins.bool] = None,
        disable_flowlog: typing.Optional[builtins.bool] = None,
        internet_gateway: typing.Optional[builtins.bool] = None,
        ipam_pool_id: typing.Optional[builtins.str] = None,
        netmask_length: typing.Optional[jsii.Number] = None,
        one_minute_flow_logs: typing.Optional[builtins.bool] = None,
        r53_internal_zone_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for Creating an enterprise Vpc which extend ec2.Vpc.

        :param availability_zones: Availability zones this VPC spans. Specify this option only if you do not specify ``maxAzs``. Default: - a subset of AZs of the stack
        :param cidr: The CIDR range to use for the VPC, e.g. '10.0.0.0/16'. Should be a minimum of /28 and maximum size of /16. The range will be split across all subnets per Availability Zone. Default: Vpc.DEFAULT_CIDR_RANGE
        :param default_instance_tenancy: The default tenancy of instances launched into the VPC. By setting this to dedicated tenancy, instances will be launched on hardware dedicated to a single AWS customer, unless specifically specified at instance launch time. Please note, not all instance types are usable with Dedicated tenancy. Default: DefaultInstanceTenancy.Default (shared) tenancy
        :param enable_dns_hostnames: Indicates whether the instances launched in the VPC get public DNS hostnames. If this attribute is true, instances in the VPC get public DNS hostnames, but only if the enableDnsSupport attribute is also set to true. Default: true
        :param enable_dns_support: Indicates whether the DNS resolution is supported for the VPC. If this attribute is false, the Amazon-provided DNS server in the VPC that resolves public DNS hostnames to IP addresses is not enabled. If this attribute is true, queries to the Amazon provided DNS server at the 169.254.169.253 IP address, or the reserved IP address at the base of the VPC IPv4 network range plus two will succeed. Default: true
        :param flow_logs: Flow logs to add to this VPC. Default: - No flow logs.
        :param gateway_endpoints: Gateway endpoints to add to this VPC. Default: - None.
        :param max_azs: Define the maximum number of AZs to use in this region. If the region has more AZs than you want to use (for example, because of EIP limits), pick a lower number here. The AZs will be sorted and picked from the start of the list. If you pick a higher number than the number of AZs in the region, all AZs in the region will be selected. To use "all AZs" available to your account, use a high number (such as 99). Be aware that environment-agnostic stacks will be created with access to only 2 AZs, so to use more than 2 AZs, be sure to specify the account and region on your stack. Specify this option only if you do not specify ``availabilityZones``. Default: 3
        :param nat_gateway_provider: What type of NAT provider to use. Select between NAT gateways or NAT instances. NAT gateways may not be available in all AWS regions. Default: NatProvider.gateway()
        :param nat_gateways: The number of NAT Gateways/Instances to create. The type of NAT gateway or instance will be determined by the ``natGatewayProvider`` parameter. You can set this number lower than the number of Availability Zones in your VPC in order to save on NAT cost. Be aware you may be charged for cross-AZ data traffic instead. Default: - One NAT gateway/instance per Availability Zone
        :param nat_gateway_subnets: Configures the subnets which will have NAT Gateways/Instances. You can pick a specific group of subnets by specifying the group name; the picked subnets must be public subnets. Only necessary if you have more than one public subnet group. Default: - All public subnets.
        :param subnet_configuration: Configure the subnets to build for each AZ. Each entry in this list configures a Subnet Group; each group will contain a subnet for each Availability Zone. For example, if you want 1 public subnet, 1 private subnet, and 1 isolated subnet in each AZ provide the following:: new ec2.Vpc(this, 'VPC', { subnetConfiguration: [ { cidrMask: 24, name: 'ingress', subnetType: ec2.SubnetType.PUBLIC, }, { cidrMask: 24, name: 'application', subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS, }, { cidrMask: 28, name: 'rds', subnetType: ec2.SubnetType.PRIVATE_ISOLATED, } ] }); Default: - The VPC CIDR will be evenly divided between 1 public and 1 private subnet per AZ.
        :param vpc_name: The VPC name. Since the VPC resource doesn't support providing a physical name, the value provided here will be recorded in the ``Name`` tag Default: this.node.path
        :param vpn_connections: VPN connections to this VPC. Default: - No connections.
        :param vpn_gateway: Indicates whether a VPN gateway should be created and attached to this VPC. Default: - true when vpnGatewayAsn or vpnConnections is specified
        :param vpn_gateway_asn: The private Autonomous System Number (ASN) for the VPN gateway. Default: - Amazon default ASN.
        :param vpn_route_propagation: Where to propagate VPN routes. Default: - On the route tables associated with private subnets. If no private subnets exists, isolated subnets are used. If no isolated subnets exists, public subnets are used.
        :param attach_to_core_network_segment: (experimental) the cloudwan core network segment name that this vpc will be attached to.
        :param central_resolving_vpc: (experimental) Set true if this is the central resolving Vpc.
        :param disable_flowlog: (experimental) Set true to disable centralised Flow Logs.
        :param internet_gateway: (experimental) An Internet Gateway will only be created if true.
        :param ipam_pool_id: (experimental) the ipam pool id that the Vpc's allocation will get created in.
        :param netmask_length: (experimental) a netmask value that is in the range 16 to 28.
        :param one_minute_flow_logs: (experimental) Set true for 1 minute aggregation on flow logs. (default is 10 minutes )
        :param r53_internal_zone_name: (experimental) Name of an internal Route53 Zone that is associated with this voc.

        :stability: experimental
        '''
        if isinstance(nat_gateway_subnets, dict):
            nat_gateway_subnets = aws_cdk.aws_ec2.SubnetSelection(**nat_gateway_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(EvpcProps.__init__)
            check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument default_instance_tenancy", value=default_instance_tenancy, expected_type=type_hints["default_instance_tenancy"])
            check_type(argname="argument enable_dns_hostnames", value=enable_dns_hostnames, expected_type=type_hints["enable_dns_hostnames"])
            check_type(argname="argument enable_dns_support", value=enable_dns_support, expected_type=type_hints["enable_dns_support"])
            check_type(argname="argument flow_logs", value=flow_logs, expected_type=type_hints["flow_logs"])
            check_type(argname="argument gateway_endpoints", value=gateway_endpoints, expected_type=type_hints["gateway_endpoints"])
            check_type(argname="argument max_azs", value=max_azs, expected_type=type_hints["max_azs"])
            check_type(argname="argument nat_gateway_provider", value=nat_gateway_provider, expected_type=type_hints["nat_gateway_provider"])
            check_type(argname="argument nat_gateways", value=nat_gateways, expected_type=type_hints["nat_gateways"])
            check_type(argname="argument nat_gateway_subnets", value=nat_gateway_subnets, expected_type=type_hints["nat_gateway_subnets"])
            check_type(argname="argument subnet_configuration", value=subnet_configuration, expected_type=type_hints["subnet_configuration"])
            check_type(argname="argument vpc_name", value=vpc_name, expected_type=type_hints["vpc_name"])
            check_type(argname="argument vpn_connections", value=vpn_connections, expected_type=type_hints["vpn_connections"])
            check_type(argname="argument vpn_gateway", value=vpn_gateway, expected_type=type_hints["vpn_gateway"])
            check_type(argname="argument vpn_gateway_asn", value=vpn_gateway_asn, expected_type=type_hints["vpn_gateway_asn"])
            check_type(argname="argument vpn_route_propagation", value=vpn_route_propagation, expected_type=type_hints["vpn_route_propagation"])
            check_type(argname="argument attach_to_core_network_segment", value=attach_to_core_network_segment, expected_type=type_hints["attach_to_core_network_segment"])
            check_type(argname="argument central_resolving_vpc", value=central_resolving_vpc, expected_type=type_hints["central_resolving_vpc"])
            check_type(argname="argument disable_flowlog", value=disable_flowlog, expected_type=type_hints["disable_flowlog"])
            check_type(argname="argument internet_gateway", value=internet_gateway, expected_type=type_hints["internet_gateway"])
            check_type(argname="argument ipam_pool_id", value=ipam_pool_id, expected_type=type_hints["ipam_pool_id"])
            check_type(argname="argument netmask_length", value=netmask_length, expected_type=type_hints["netmask_length"])
            check_type(argname="argument one_minute_flow_logs", value=one_minute_flow_logs, expected_type=type_hints["one_minute_flow_logs"])
            check_type(argname="argument r53_internal_zone_name", value=r53_internal_zone_name, expected_type=type_hints["r53_internal_zone_name"])
        self._values: typing.Dict[str, typing.Any] = {}
        if availability_zones is not None:
            self._values["availability_zones"] = availability_zones
        if cidr is not None:
            self._values["cidr"] = cidr
        if default_instance_tenancy is not None:
            self._values["default_instance_tenancy"] = default_instance_tenancy
        if enable_dns_hostnames is not None:
            self._values["enable_dns_hostnames"] = enable_dns_hostnames
        if enable_dns_support is not None:
            self._values["enable_dns_support"] = enable_dns_support
        if flow_logs is not None:
            self._values["flow_logs"] = flow_logs
        if gateway_endpoints is not None:
            self._values["gateway_endpoints"] = gateway_endpoints
        if max_azs is not None:
            self._values["max_azs"] = max_azs
        if nat_gateway_provider is not None:
            self._values["nat_gateway_provider"] = nat_gateway_provider
        if nat_gateways is not None:
            self._values["nat_gateways"] = nat_gateways
        if nat_gateway_subnets is not None:
            self._values["nat_gateway_subnets"] = nat_gateway_subnets
        if subnet_configuration is not None:
            self._values["subnet_configuration"] = subnet_configuration
        if vpc_name is not None:
            self._values["vpc_name"] = vpc_name
        if vpn_connections is not None:
            self._values["vpn_connections"] = vpn_connections
        if vpn_gateway is not None:
            self._values["vpn_gateway"] = vpn_gateway
        if vpn_gateway_asn is not None:
            self._values["vpn_gateway_asn"] = vpn_gateway_asn
        if vpn_route_propagation is not None:
            self._values["vpn_route_propagation"] = vpn_route_propagation
        if attach_to_core_network_segment is not None:
            self._values["attach_to_core_network_segment"] = attach_to_core_network_segment
        if central_resolving_vpc is not None:
            self._values["central_resolving_vpc"] = central_resolving_vpc
        if disable_flowlog is not None:
            self._values["disable_flowlog"] = disable_flowlog
        if internet_gateway is not None:
            self._values["internet_gateway"] = internet_gateway
        if ipam_pool_id is not None:
            self._values["ipam_pool_id"] = ipam_pool_id
        if netmask_length is not None:
            self._values["netmask_length"] = netmask_length
        if one_minute_flow_logs is not None:
            self._values["one_minute_flow_logs"] = one_minute_flow_logs
        if r53_internal_zone_name is not None:
            self._values["r53_internal_zone_name"] = r53_internal_zone_name

    @builtins.property
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Availability zones this VPC spans.

        Specify this option only if you do not specify ``maxAzs``.

        :default: - a subset of AZs of the stack
        '''
        result = self._values.get("availability_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cidr(self) -> typing.Optional[builtins.str]:
        '''The CIDR range to use for the VPC, e.g. '10.0.0.0/16'.

        Should be a minimum of /28 and maximum size of /16. The range will be
        split across all subnets per Availability Zone.

        :default: Vpc.DEFAULT_CIDR_RANGE
        '''
        result = self._values.get("cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_instance_tenancy(
        self,
    ) -> typing.Optional[aws_cdk.aws_ec2.DefaultInstanceTenancy]:
        '''The default tenancy of instances launched into the VPC.

        By setting this to dedicated tenancy, instances will be launched on
        hardware dedicated to a single AWS customer, unless specifically specified
        at instance launch time. Please note, not all instance types are usable
        with Dedicated tenancy.

        :default: DefaultInstanceTenancy.Default (shared) tenancy
        '''
        result = self._values.get("default_instance_tenancy")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.DefaultInstanceTenancy], result)

    @builtins.property
    def enable_dns_hostnames(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether the instances launched in the VPC get public DNS hostnames.

        If this attribute is true, instances in the VPC get public DNS hostnames,
        but only if the enableDnsSupport attribute is also set to true.

        :default: true
        '''
        result = self._values.get("enable_dns_hostnames")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_dns_support(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether the DNS resolution is supported for the VPC.

        If this attribute is false, the Amazon-provided DNS server in the VPC that
        resolves public DNS hostnames to IP addresses is not enabled. If this
        attribute is true, queries to the Amazon provided DNS server at the
        169.254.169.253 IP address, or the reserved IP address at the base of the
        VPC IPv4 network range plus two will succeed.

        :default: true
        '''
        result = self._values.get("enable_dns_support")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def flow_logs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_ec2.FlowLogOptions]]:
        '''Flow logs to add to this VPC.

        :default: - No flow logs.
        '''
        result = self._values.get("flow_logs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_ec2.FlowLogOptions]], result)

    @builtins.property
    def gateway_endpoints(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_ec2.GatewayVpcEndpointOptions]]:
        '''Gateway endpoints to add to this VPC.

        :default: - None.
        '''
        result = self._values.get("gateway_endpoints")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_ec2.GatewayVpcEndpointOptions]], result)

    @builtins.property
    def max_azs(self) -> typing.Optional[jsii.Number]:
        '''Define the maximum number of AZs to use in this region.

        If the region has more AZs than you want to use (for example, because of
        EIP limits), pick a lower number here. The AZs will be sorted and picked
        from the start of the list.

        If you pick a higher number than the number of AZs in the region, all AZs
        in the region will be selected. To use "all AZs" available to your
        account, use a high number (such as 99).

        Be aware that environment-agnostic stacks will be created with access to
        only 2 AZs, so to use more than 2 AZs, be sure to specify the account and
        region on your stack.

        Specify this option only if you do not specify ``availabilityZones``.

        :default: 3
        '''
        result = self._values.get("max_azs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nat_gateway_provider(self) -> typing.Optional[aws_cdk.aws_ec2.NatProvider]:
        '''What type of NAT provider to use.

        Select between NAT gateways or NAT instances. NAT gateways
        may not be available in all AWS regions.

        :default: NatProvider.gateway()
        '''
        result = self._values.get("nat_gateway_provider")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.NatProvider], result)

    @builtins.property
    def nat_gateways(self) -> typing.Optional[jsii.Number]:
        '''The number of NAT Gateways/Instances to create.

        The type of NAT gateway or instance will be determined by the
        ``natGatewayProvider`` parameter.

        You can set this number lower than the number of Availability Zones in your
        VPC in order to save on NAT cost. Be aware you may be charged for
        cross-AZ data traffic instead.

        :default: - One NAT gateway/instance per Availability Zone
        '''
        result = self._values.get("nat_gateways")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nat_gateway_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        '''Configures the subnets which will have NAT Gateways/Instances.

        You can pick a specific group of subnets by specifying the group name;
        the picked subnets must be public subnets.

        Only necessary if you have more than one public subnet group.

        :default: - All public subnets.
        '''
        result = self._values.get("nat_gateway_subnets")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.SubnetSelection], result)

    @builtins.property
    def subnet_configuration(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ec2.SubnetConfiguration]]:
        '''Configure the subnets to build for each AZ.

        Each entry in this list configures a Subnet Group; each group will contain a
        subnet for each Availability Zone.

        For example, if you want 1 public subnet, 1 private subnet, and 1 isolated
        subnet in each AZ provide the following::

           new ec2.Vpc(this, 'VPC', {
              subnetConfiguration: [
                 {
                   cidrMask: 24,
                   name: 'ingress',
                   subnetType: ec2.SubnetType.PUBLIC,
                 },
                 {
                   cidrMask: 24,
                   name: 'application',
                   subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
                 },
                 {
                   cidrMask: 28,
                   name: 'rds',
                   subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
                 }
              ]
           });

        :default:

        - The VPC CIDR will be evenly divided between 1 public and 1
        private subnet per AZ.
        '''
        result = self._values.get("subnet_configuration")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_ec2.SubnetConfiguration]], result)

    @builtins.property
    def vpc_name(self) -> typing.Optional[builtins.str]:
        '''The VPC name.

        Since the VPC resource doesn't support providing a physical name, the value provided here will be recorded in the ``Name`` tag

        :default: this.node.path
        '''
        result = self._values.get("vpc_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpn_connections(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_ec2.VpnConnectionOptions]]:
        '''VPN connections to this VPC.

        :default: - No connections.
        '''
        result = self._values.get("vpn_connections")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_ec2.VpnConnectionOptions]], result)

    @builtins.property
    def vpn_gateway(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether a VPN gateway should be created and attached to this VPC.

        :default: - true when vpnGatewayAsn or vpnConnections is specified
        '''
        result = self._values.get("vpn_gateway")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpn_gateway_asn(self) -> typing.Optional[jsii.Number]:
        '''The private Autonomous System Number (ASN) for the VPN gateway.

        :default: - Amazon default ASN.
        '''
        result = self._values.get("vpn_gateway_asn")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpn_route_propagation(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ec2.SubnetSelection]]:
        '''Where to propagate VPN routes.

        :default:

        - On the route tables associated with private subnets. If no
        private subnets exists, isolated subnets are used. If no isolated subnets
        exists, public subnets are used.
        '''
        result = self._values.get("vpn_route_propagation")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_ec2.SubnetSelection]], result)

    @builtins.property
    def attach_to_core_network_segment(self) -> typing.Optional[builtins.str]:
        '''(experimental) the cloudwan core network segment name that this vpc will be attached to.

        :stability: experimental
        '''
        result = self._values.get("attach_to_core_network_segment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def central_resolving_vpc(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Set true if this is the central resolving Vpc.

        :stability: experimental
        '''
        result = self._values.get("central_resolving_vpc")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def disable_flowlog(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Set true to disable centralised Flow Logs.

        :stability: experimental
        '''
        result = self._values.get("disable_flowlog")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def internet_gateway(self) -> typing.Optional[builtins.bool]:
        '''(experimental) An Internet Gateway will only be created if true.

        :stability: experimental
        '''
        result = self._values.get("internet_gateway")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ipam_pool_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) the ipam pool id that the Vpc's allocation will get created in.

        :stability: experimental
        '''
        result = self._values.get("ipam_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def netmask_length(self) -> typing.Optional[jsii.Number]:
        '''(experimental) a netmask value that is in the range 16 to 28.

        :stability: experimental
        '''
        result = self._values.get("netmask_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def one_minute_flow_logs(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Set true for 1 minute aggregation on flow logs.

        (default is 10 minutes )

        :stability: experimental
        '''
        result = self._values.get("one_minute_flow_logs")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def r53_internal_zone_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of an internal Route53 Zone that is associated with this voc.

        :stability: experimental
        '''
        result = self._values.get("r53_internal_zone_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EvpcProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GetTunnelAddressPair(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.GetTunnelAddressPair",
):
    '''(experimental) Allocate a pair of /30 networks CIDRS for use in Ipsec VPN Tunnels.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        ipam_pool_id: builtins.str,
        name: builtins.str,
    ) -> None:
        '''
        :param scope: scope in which this resource is created.
        :param id: scope id of the resoruce.
        :param ipam_pool_id: (experimental) The IPAM Pool Id from which the assginment will be made from.
        :param name: (experimental) The Name used by IPAM to record the allocation.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(GetTunnelAddressPair.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GetTunnelAddressPairProps(ipam_pool_id=ipam_pool_id, name=name)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="assignedCidrPair")
    def assigned_cidr_pair(self) -> typing.List[builtins.str]:
        '''(experimental) returns 2 cidr blocks as an array to be used by an IPsec Tunnel.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "assignedCidrPair"))


@jsii.data_type(
    jsii_type="raindancers-network.GetTunnelAddressPairProps",
    jsii_struct_bases=[],
    name_mapping={"ipam_pool_id": "ipamPoolId", "name": "name"},
)
class GetTunnelAddressPairProps:
    def __init__(self, *, ipam_pool_id: builtins.str, name: builtins.str) -> None:
        '''(experimental) Properties for obtaining an IPAM assigned address pair for use on IPsec VPN Tunnels.

        :param ipam_pool_id: (experimental) The IPAM Pool Id from which the assginment will be made from.
        :param name: (experimental) The Name used by IPAM to record the allocation.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(GetTunnelAddressPairProps.__init__)
            check_type(argname="argument ipam_pool_id", value=ipam_pool_id, expected_type=type_hints["ipam_pool_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[str, typing.Any] = {
            "ipam_pool_id": ipam_pool_id,
            "name": name,
        }

    @builtins.property
    def ipam_pool_id(self) -> builtins.str:
        '''(experimental) The IPAM Pool Id from which the assginment will be made from.

        :stability: experimental
        '''
        result = self._values.get("ipam_pool_id")
        assert result is not None, "Required property 'ipam_pool_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The Name used by IPAM to record the allocation.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GetTunnelAddressPairProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="raindancers-network.ICoreNetworkSegmentProps")
class ICoreNetworkSegmentProps(typing_extensions.Protocol):
    '''(experimental) Properties creating a Corenetwork Segment.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="policyTableServiceToken")
    def policy_table_service_token(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="segmentName")
    def segment_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="updateDependsOn")
    def update_depends_on(self) -> typing.List[aws_cdk.CustomResource]:
        '''
        :stability: experimental
        '''
        ...

    @update_depends_on.setter
    def update_depends_on(self, value: typing.List[aws_cdk.CustomResource]) -> None:
        ...


class _ICoreNetworkSegmentPropsProxy:
    '''(experimental) Properties creating a Corenetwork Segment.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "raindancers-network.ICoreNetworkSegmentProps"

    @builtins.property
    @jsii.member(jsii_name="policyTableServiceToken")
    def policy_table_service_token(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "policyTableServiceToken"))

    @builtins.property
    @jsii.member(jsii_name="segmentName")
    def segment_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "segmentName"))

    @builtins.property
    @jsii.member(jsii_name="updateDependsOn")
    def update_depends_on(self) -> typing.List[aws_cdk.CustomResource]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[aws_cdk.CustomResource], jsii.get(self, "updateDependsOn"))

    @update_depends_on.setter
    def update_depends_on(self, value: typing.List[aws_cdk.CustomResource]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(ICoreNetworkSegmentProps, "update_depends_on").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updateDependsOn", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICoreNetworkSegmentProps).__jsii_proxy_class__ = lambda : _ICoreNetworkSegmentPropsProxy


class IpsecTunnelPool(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.IpsecTunnelPool",
):
    '''(experimental) Creates an IPAM pool to assign address's for IPsec VPNS.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cidr: builtins.str,
        description: builtins.str,
        ipam_scope_id: builtins.str,
        name: builtins.str,
    ) -> None:
        '''
        :param scope: scope in which this resource is defined.
        :param id: id of the resource.
        :param cidr: (experimental) The Cidr range for pools to be created from eg, 169.254.100.0/27 The cidr must be in the 169.254.0.0/16 range and must be a minimum of a /29 and a maximum of /24. It must also not overlap the AWS reserved ranges. T
        :param description: (experimental) the description used by IPAM to describe the pool.
        :param ipam_scope_id: (experimental) The IPAM Scope Id to use to create the Pool.
        :param name: (experimental) the name used by IPAM to identify the pool.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(IpsecTunnelPool.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = IpsecTunnelPoolProps(
            cidr=cidr, description=description, ipam_scope_id=ipam_scope_id, name=name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="ipampool")
    def ipampool(self) -> aws_cdk.aws_ec2.CfnIPAMPool:
        '''(experimental) returns the created ipam Pool.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_ec2.CfnIPAMPool, jsii.get(self, "ipampool"))


@jsii.data_type(
    jsii_type="raindancers-network.IpsecTunnelPoolProps",
    jsii_struct_bases=[],
    name_mapping={
        "cidr": "cidr",
        "description": "description",
        "ipam_scope_id": "ipamScopeId",
        "name": "name",
    },
)
class IpsecTunnelPoolProps:
    def __init__(
        self,
        *,
        cidr: builtins.str,
        description: builtins.str,
        ipam_scope_id: builtins.str,
        name: builtins.str,
    ) -> None:
        '''(experimental) Properties for defining a IPAM Pool specifically for IPSec VPN Tunnels.

        :param cidr: (experimental) The Cidr range for pools to be created from eg, 169.254.100.0/27 The cidr must be in the 169.254.0.0/16 range and must be a minimum of a /29 and a maximum of /24. It must also not overlap the AWS reserved ranges. T
        :param description: (experimental) the description used by IPAM to describe the pool.
        :param ipam_scope_id: (experimental) The IPAM Scope Id to use to create the Pool.
        :param name: (experimental) the name used by IPAM to identify the pool.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(IpsecTunnelPoolProps.__init__)
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument ipam_scope_id", value=ipam_scope_id, expected_type=type_hints["ipam_scope_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[str, typing.Any] = {
            "cidr": cidr,
            "description": description,
            "ipam_scope_id": ipam_scope_id,
            "name": name,
        }

    @builtins.property
    def cidr(self) -> builtins.str:
        '''(experimental) The Cidr range for pools to be created from    eg, 169.254.100.0/27 The cidr must be in the 169.254.0.0/16 range and must be a minimum of a /29 and a maximum of /24.

        It must also not overlap the AWS reserved ranges. T

        :stability: experimental
        '''
        result = self._values.get("cidr")
        assert result is not None, "Required property 'cidr' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> builtins.str:
        '''(experimental) the description used by IPAM to describe the pool.

        :stability: experimental
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ipam_scope_id(self) -> builtins.str:
        '''(experimental) The IPAM Scope Id to use to create the Pool.

        :stability: experimental
        '''
        result = self._values.get("ipam_scope_id")
        assert result is not None, "Required property 'ipam_scope_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) the name used by IPAM to identify the pool.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IpsecTunnelPoolProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="raindancers-network.Operators")
class Operators(enum.Enum):
    '''(experimental) Operatior COnditons for Attachments.

    :stability: experimental
    '''

    EQUALS = "EQUALS"
    '''
    :stability: experimental
    '''
    NOTEQUALS = "NOTEQUALS"
    '''
    :stability: experimental
    '''
    CONTAINS = "CONTAINS"
    '''
    :stability: experimental
    '''
    BEGINS_WITH = "BEGINS_WITH"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="raindancers-network.Segment",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "allow_filter": "allowFilter",
        "deny_filter": "denyFilter",
        "description": "description",
        "edge_locations": "edgeLocations",
        "isolate_attachments": "isolateAttachments",
        "require_attachment_acceptance": "requireAttachmentAcceptance",
    },
)
class Segment:
    def __init__(
        self,
        *,
        name: builtins.str,
        allow_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        deny_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        edge_locations: typing.Optional[typing.Sequence[typing.Mapping[typing.Any, typing.Any]]] = None,
        isolate_attachments: typing.Optional[builtins.bool] = None,
        require_attachment_acceptance: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Segment Properties.

        :param name: (experimental) Name of the Segment.
        :param allow_filter: (experimental) A list of denys.
        :param deny_filter: (experimental) a List of denys.
        :param description: (experimental) A description of the of the segement.
        :param edge_locations: (experimental) A list of edge locations where the segement will be avaialble. Not that the locations must also be included in the core network edge ( CNE )
        :param isolate_attachments: (experimental) Set true if attached VPCS are isolated from each other.
        :param require_attachment_acceptance: (experimental) Set true if the attachment needs approval for connection. Currently not supported and requires an automation step

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Segment.__init__)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allow_filter", value=allow_filter, expected_type=type_hints["allow_filter"])
            check_type(argname="argument deny_filter", value=deny_filter, expected_type=type_hints["deny_filter"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument edge_locations", value=edge_locations, expected_type=type_hints["edge_locations"])
            check_type(argname="argument isolate_attachments", value=isolate_attachments, expected_type=type_hints["isolate_attachments"])
            check_type(argname="argument require_attachment_acceptance", value=require_attachment_acceptance, expected_type=type_hints["require_attachment_acceptance"])
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if allow_filter is not None:
            self._values["allow_filter"] = allow_filter
        if deny_filter is not None:
            self._values["deny_filter"] = deny_filter
        if description is not None:
            self._values["description"] = description
        if edge_locations is not None:
            self._values["edge_locations"] = edge_locations
        if isolate_attachments is not None:
            self._values["isolate_attachments"] = isolate_attachments
        if require_attachment_acceptance is not None:
            self._values["require_attachment_acceptance"] = require_attachment_acceptance

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) Name of the Segment.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_filter(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of denys.

        :stability: experimental
        '''
        result = self._values.get("allow_filter")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def deny_filter(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) a List of denys.

        :stability: experimental
        '''
        result = self._values.get("deny_filter")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the of the segement.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def edge_locations(
        self,
    ) -> typing.Optional[typing.List[typing.Mapping[typing.Any, typing.Any]]]:
        '''(experimental) A list of edge locations where the segement will be avaialble.

        Not that the
        locations must also be included in the core network edge ( CNE )

        :stability: experimental
        '''
        result = self._values.get("edge_locations")
        return typing.cast(typing.Optional[typing.List[typing.Mapping[typing.Any, typing.Any]]], result)

    @builtins.property
    def isolate_attachments(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Set true if attached VPCS are isolated from each other.

        :stability: experimental
        '''
        result = self._values.get("isolate_attachments")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def require_attachment_acceptance(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Set true if the attachment needs approval for connection.

        Currently not supported
        and requires an automation step

        :stability: experimental
        '''
        result = self._values.get("require_attachment_acceptance")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Segment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.SegmentAction",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "description": "description",
        "destination_cidr_blocks": "destinationCidrBlocks",
        "destinations": "destinations",
        "except_": "except",
        "mode": "mode",
        "share_with": "shareWith",
    },
)
class SegmentAction:
    def __init__(
        self,
        *,
        action: "SegmentActionType",
        description: builtins.str,
        destination_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
        destinations: typing.Optional[typing.Sequence[builtins.str]] = None,
        except_: typing.Optional[typing.Sequence[builtins.str]] = None,
        mode: typing.Optional["SegmentActionMode"] = None,
        share_with: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Segmment ACtions.

        :param action: 
        :param description: 
        :param destination_cidr_blocks: 
        :param destinations: 
        :param except_: 
        :param mode: 
        :param share_with: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SegmentAction.__init__)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument destination_cidr_blocks", value=destination_cidr_blocks, expected_type=type_hints["destination_cidr_blocks"])
            check_type(argname="argument destinations", value=destinations, expected_type=type_hints["destinations"])
            check_type(argname="argument except_", value=except_, expected_type=type_hints["except_"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument share_with", value=share_with, expected_type=type_hints["share_with"])
        self._values: typing.Dict[str, typing.Any] = {
            "action": action,
            "description": description,
        }
        if destination_cidr_blocks is not None:
            self._values["destination_cidr_blocks"] = destination_cidr_blocks
        if destinations is not None:
            self._values["destinations"] = destinations
        if except_ is not None:
            self._values["except_"] = except_
        if mode is not None:
            self._values["mode"] = mode
        if share_with is not None:
            self._values["share_with"] = share_with

    @builtins.property
    def action(self) -> "SegmentActionType":
        '''
        :stability: experimental
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast("SegmentActionType", result)

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_cidr_blocks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("destination_cidr_blocks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def destinations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("destinations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def except_(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("except_")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def mode(self) -> typing.Optional["SegmentActionMode"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional["SegmentActionMode"], result)

    @builtins.property
    def share_with(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("share_with")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SegmentAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="raindancers-network.SegmentActionMode")
class SegmentActionMode(enum.Enum):
    '''(experimental) Segment Action Mode.

    :stability: experimental
    '''

    ATTACHMENT_ROUTE = "ATTACHMENT_ROUTE"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="raindancers-network.SegmentActionType")
class SegmentActionType(enum.Enum):
    '''(experimental) Segment Action Type.

    :stability: experimental
    '''

    SHARE = "SHARE"
    '''
    :stability: experimental
    '''
    CREATE_ROUTE = "CREATE_ROUTE"
    '''
    :stability: experimental
    '''


__all__ = [
    "AssociationMethod",
    "AttachmentCondition",
    "AttachmentConditions",
    "AttachmentPolicy",
    "AttachmentPolicyAction",
    "ConditionLogic",
    "CoreNetwork",
    "CoreNetworkProps",
    "CoreNetworkShare",
    "Evpc",
    "EvpcProps",
    "GetTunnelAddressPair",
    "GetTunnelAddressPairProps",
    "ICoreNetworkSegmentProps",
    "IpsecTunnelPool",
    "IpsecTunnelPoolProps",
    "Operators",
    "Segment",
    "SegmentAction",
    "SegmentActionMode",
    "SegmentActionType",
]

publication.publish()
