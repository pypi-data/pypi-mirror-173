'''
<div align="center">
	<br/>
	<br/>
  <h1>
	<img height="140" src="assets/alma-cdk-aws-interface-endpoints.svg" alt="Alma CDK Domain" />
  <br/>
  <br/>
  </h1>

```sh
npm i -D @alma-cdk/aws-interface-endpoints
```

  <div align="left">

L3 construct helping with PrivateLink-powered VPC Interface Endpoints for AWS Services.

  </div>
  <br/>
</div><br/>

## 🚧   Project Stability

![experimental](https://img.shields.io/badge/stability-experimental-yellow)

This construct is still versioned with `v0` major version and breaking changes might be introduced if necessary (without a major version bump), though we aim to keep the API as stable as possible (even within `v0` development). We aim to publish `v1.0.0` soon and after that breaking changes will be introduced via major version bumps.

<br/>

## Getting Started

### Endpoint open to whole isolated subnet

```python
import { AwsInterfaceEndpoints } from '@alma-cdk/aws-interface-endpoints';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
```

```python
const vpc = new ec2.Vpc();

new AwsInterfaceEndpoints(this, 'EcrInterfaceEndpoint', {
  vpc,
  services: [
    ec2.InterfaceVpcEndpointAwsService.ECR_DOCKER,
  ],
});
```

### Session Manager connection endpoints

```python
import { AwsInterfaceEndpoints } from '@alma-cdk/aws-interface-endpoints';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
```

```python
const vpc = new ec2.Vpc();

new AwsInterfaceEndpoints(this, 'SessionManagerInterfaceEndpoint', {
  vpc,
  services: AwsInterfaceEndpoints.SessionManagerConnect,
});
```

### Explictly opened endpoints

1. In your VPC creation stack

```python
import { AwsInterfaceEndpoints } from '@alma-cdk/aws-interface-endpoints';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
```

```python
const vpc = new ec2.Vpc();

new AwsInterfaceEndpoints(this, 'EcrInterfaceEndpoint', {
  vpc,
  open: false,
  services: [
    ec2.InterfaceVpcEndpointAwsService.ECR_DOCKER,
  ],
});
```

1. In some other stack (maybe on a completely different CDK application):

```python
import { AwsInterfaceEndpoints } from '@alma-cdk/aws-interface-endpoints';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
```

```python
define instance: ec2.Instance;

const endpoints = AwsInterfaceEndpoints.fromAttributes(this, 'EcrInterfaceEndpoint', {
  services: [
    ec2.InterfaceVpcEndpointAwsService.ECR_DOCKER,
  ],
});

endpoints.allowDefaultPromFrom(instance);
```

<br/>

https://docs.aws.amazon.com/systems-manager/latest/userguide/setup-create-vpc.html

https://aws.amazon.com/privatelink/pricing/

https://docs.aws.amazon.com/vpc/latest/privatelink/create-interface-endpoint.html
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

import aws_cdk.aws_ec2
import constructs


@jsii.interface(jsii_type="@alma-cdk/aws-interface-endpoints.IAwsInterfaceEndpoints")
class IAwsInterfaceEndpoints(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="allowDefaultPromFrom")
    def allow_default_prom_from(
        self,
        connectable: aws_cdk.aws_ec2.IConnectable,
    ) -> None:
        '''
        :param connectable: -

        :stability: experimental
        '''
        ...


class _IAwsInterfaceEndpointsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@alma-cdk/aws-interface-endpoints.IAwsInterfaceEndpoints"

    @jsii.member(jsii_name="allowDefaultPromFrom")
    def allow_default_prom_from(
        self,
        connectable: aws_cdk.aws_ec2.IConnectable,
    ) -> None:
        '''
        :param connectable: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(IAwsInterfaceEndpoints.allow_default_prom_from)
            check_type(argname="argument connectable", value=connectable, expected_type=type_hints["connectable"])
        return typing.cast(None, jsii.invoke(self, "allowDefaultPromFrom", [connectable]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAwsInterfaceEndpoints).__jsii_proxy_class__ = lambda : _IAwsInterfaceEndpointsProxy


@jsii.data_type(
    jsii_type="@alma-cdk/aws-interface-endpoints.LookupProps",
    jsii_struct_bases=[],
    name_mapping={"services": "services", "export_prefix": "exportPrefix"},
)
class LookupProps:
    def __init__(
        self,
        *,
        services: typing.Sequence[aws_cdk.aws_ec2.InterfaceVpcEndpointAwsService],
        export_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param services: 
        :param export_prefix: (experimental) Prefix used to identity CloudFormation cross-stack exports. Default: 'SessionManagerEndpoints'

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(LookupProps.__init__)
            check_type(argname="argument services", value=services, expected_type=type_hints["services"])
            check_type(argname="argument export_prefix", value=export_prefix, expected_type=type_hints["export_prefix"])
        self._values: typing.Dict[str, typing.Any] = {
            "services": services,
        }
        if export_prefix is not None:
            self._values["export_prefix"] = export_prefix

    @builtins.property
    def services(self) -> typing.List[aws_cdk.aws_ec2.InterfaceVpcEndpointAwsService]:
        '''
        :stability: experimental
        '''
        result = self._values.get("services")
        assert result is not None, "Required property 'services' is missing"
        return typing.cast(typing.List[aws_cdk.aws_ec2.InterfaceVpcEndpointAwsService], result)

    @builtins.property
    def export_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) Prefix used to identity CloudFormation cross-stack exports.

        :default: 'SessionManagerEndpoints'

        :stability: experimental
        '''
        result = self._values.get("export_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LookupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@alma-cdk/aws-interface-endpoints.SessionManagerEndpointProps",
    jsii_struct_bases=[],
    name_mapping={
        "services": "services",
        "vpc": "vpc",
        "export_prefix": "exportPrefix",
        "open": "open",
        "security_groups": "securityGroups",
        "subnets": "subnets",
    },
)
class SessionManagerEndpointProps:
    def __init__(
        self,
        *,
        services: typing.Sequence[aws_cdk.aws_ec2.InterfaceVpcEndpointAwsService],
        vpc: aws_cdk.aws_ec2.IVpc,
        export_prefix: typing.Optional[builtins.str] = None,
        open: typing.Optional[builtins.bool] = None,
        security_groups: typing.Optional[typing.Sequence[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param services: 
        :param vpc: (experimental) To which VPC these endpoints are assigned.
        :param export_prefix: (experimental) Prefix used to identity CloudFormation cross-stack exports. Default: 'SessionManagerEndpoints'
        :param open: (experimental) Whether to automatically allow VPC traffic to the endpoint. If enabled, all traffic to the endpoint from within the VPC will be automatically allowed. This is done based on the VPC's CIDR range. Default: true
        :param security_groups: (experimental) The security groups to associate with this interface VPC endpoint. Default: - a new security group is created
        :param subnets: (experimental) To which subnets the endpoints are assigned. Default: { subnetType: ec2.SubnetType.PRIVATE_ISOLATED }

        :stability: experimental
        '''
        if isinstance(subnets, dict):
            subnets = aws_cdk.aws_ec2.SubnetSelection(**subnets)
        if __debug__:
            type_hints = typing.get_type_hints(SessionManagerEndpointProps.__init__)
            check_type(argname="argument services", value=services, expected_type=type_hints["services"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument export_prefix", value=export_prefix, expected_type=type_hints["export_prefix"])
            check_type(argname="argument open", value=open, expected_type=type_hints["open"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
        self._values: typing.Dict[str, typing.Any] = {
            "services": services,
            "vpc": vpc,
        }
        if export_prefix is not None:
            self._values["export_prefix"] = export_prefix
        if open is not None:
            self._values["open"] = open
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets

    @builtins.property
    def services(self) -> typing.List[aws_cdk.aws_ec2.InterfaceVpcEndpointAwsService]:
        '''
        :stability: experimental
        '''
        result = self._values.get("services")
        assert result is not None, "Required property 'services' is missing"
        return typing.cast(typing.List[aws_cdk.aws_ec2.InterfaceVpcEndpointAwsService], result)

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        '''(experimental) To which VPC these endpoints are assigned.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(aws_cdk.aws_ec2.IVpc, result)

    @builtins.property
    def export_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) Prefix used to identity CloudFormation cross-stack exports.

        :default: 'SessionManagerEndpoints'

        :stability: experimental
        '''
        result = self._values.get("export_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def open(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to automatically allow VPC traffic to the endpoint.

        If enabled, all traffic to the endpoint from within the VPC will be automatically allowed. This is done based on the VPC's CIDR range.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("open")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]:
        '''(experimental) The security groups to associate with this interface VPC endpoint.

        :default: - a new security group is created

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]], result)

    @builtins.property
    def subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        '''(experimental) To which subnets the endpoints are assigned.

        :default: { subnetType: ec2.SubnetType.PRIVATE_ISOLATED }

        :stability: experimental
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SessionManagerEndpointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IAwsInterfaceEndpoints)
class AwsInterfaceEndpoints(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alma-cdk/aws-interface-endpoints.AwsInterfaceEndpoints",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        services: typing.Sequence[aws_cdk.aws_ec2.InterfaceVpcEndpointAwsService],
        vpc: aws_cdk.aws_ec2.IVpc,
        export_prefix: typing.Optional[builtins.str] = None,
        open: typing.Optional[builtins.bool] = None,
        security_groups: typing.Optional[typing.Sequence[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param services: 
        :param vpc: (experimental) To which VPC these endpoints are assigned.
        :param export_prefix: (experimental) Prefix used to identity CloudFormation cross-stack exports. Default: 'SessionManagerEndpoints'
        :param open: (experimental) Whether to automatically allow VPC traffic to the endpoint. If enabled, all traffic to the endpoint from within the VPC will be automatically allowed. This is done based on the VPC's CIDR range. Default: true
        :param security_groups: (experimental) The security groups to associate with this interface VPC endpoint. Default: - a new security group is created
        :param subnets: (experimental) To which subnets the endpoints are assigned. Default: { subnetType: ec2.SubnetType.PRIVATE_ISOLATED }

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AwsInterfaceEndpoints.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SessionManagerEndpointProps(
            services=services,
            vpc=vpc,
            export_prefix=export_prefix,
            open=open,
            security_groups=security_groups,
            subnets=subnets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromAttributes")
    @builtins.classmethod
    def from_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        services: typing.Sequence[aws_cdk.aws_ec2.InterfaceVpcEndpointAwsService],
        export_prefix: typing.Optional[builtins.str] = None,
    ) -> IAwsInterfaceEndpoints:
        '''
        :param scope: -
        :param id: -
        :param services: 
        :param export_prefix: (experimental) Prefix used to identity CloudFormation cross-stack exports. Default: 'SessionManagerEndpoints'

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AwsInterfaceEndpoints.from_attributes)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LookupProps(services=services, export_prefix=export_prefix)

        return typing.cast(IAwsInterfaceEndpoints, jsii.sinvoke(cls, "fromAttributes", [scope, id, props]))

    @jsii.member(jsii_name="allowDefaultPromFrom")
    def allow_default_prom_from(
        self,
        connectable: aws_cdk.aws_ec2.IConnectable,
    ) -> None:
        '''
        :param connectable: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AwsInterfaceEndpoints.allow_default_prom_from)
            check_type(argname="argument connectable", value=connectable, expected_type=type_hints["connectable"])
        return typing.cast(None, jsii.invoke(self, "allowDefaultPromFrom", [connectable]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SessionManagerConnect")
    def SESSION_MANAGER_CONNECT(
        cls,
    ) -> typing.List[aws_cdk.aws_ec2.InterfaceVpcEndpointAwsService]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[aws_cdk.aws_ec2.InterfaceVpcEndpointAwsService], jsii.sget(cls, "SessionManagerConnect"))


__all__ = [
    "AwsInterfaceEndpoints",
    "IAwsInterfaceEndpoints",
    "LookupProps",
    "SessionManagerEndpointProps",
]

publication.publish()
