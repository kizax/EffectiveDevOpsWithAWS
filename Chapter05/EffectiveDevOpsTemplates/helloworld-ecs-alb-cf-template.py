{
    "Description": "Effective DevOps in AWS: ALB for the ECS Cluster",
    "Outputs": {
        "TargetGroup": {
            "Description": "TargetGroup",
            "Export": {
                "Name": {
                    "Fn::Sub": "${AWS::StackName}-target-group"
                }
            },
            "Value": {
                "Ref": "TargetGroup"
            }
        },
        "URL": {
            "Description": "Helloworld URL",
            "Value": {
                "Fn::Join": [
                    "",
                    [
                        "http://",
                        {
                            "Fn::GetAtt": [
                                "LoadBalancer",
                                "DNSName"
                            ]
                        },
                        ":3000"
                    ]
                ]
            }
        }
    },
    "Resources": {
        "Listener": {
            "Properties": {
                "DefaultActions": [
                    {
                        "TargetGroupArn": {
                            "Ref": "TargetGroup"
                        },
                        "Type": "forward"
                    }
                ],
                "LoadBalancerArn": {
                    "Ref": "LoadBalancer"
                },
                "Port": "3000",
                "Protocol": "HTTP"
            },
            "Type": "AWS::ElasticLoadBalancingV2::Listener"
        },
        "LoadBalancer": {
            "Properties": {
                "LoadBalancerAttributes": [
                    {
                        "Key": "access_logs.s3.enabled",
                        "Value": "true"
                    },
                    {
                        "Key": "access_logs.s3.bucket",
                        "Value": {
                            "Ref": "S3Bucket"
                        }
                    }
                ],
                "Scheme": "internet-facing",
                "SecurityGroups": [
                    {
                        "Ref": "LoadBalancerSecurityGroup"
                    }
                ],
                "Subnets": {
                    "Fn::Split": [
                        ",",
                        {
                            "Fn::ImportValue": {
                                "Fn::Join": [
                                    "-",
                                    [
                                        {
                                            "Fn::Select": [
                                                0,
                                                {
                                                    "Fn::Split": [
                                                        "-",
                                                        {
                                                            "Ref": "AWS::StackName"
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        "cluster-public-subnets"
                                    ]
                                ]
                            }
                        }
                    ]
                }
            },
            "Type": "AWS::ElasticLoadBalancingV2::LoadBalancer"
        },
        "LoadBalancerSecurityGroup": {
            "Properties": {
                "GroupDescription": "Web load balancer security group.",
                "SecurityGroupIngress": [
                    {
                        "CidrIp": "0.0.0.0/0",
                        "FromPort": "3000",
                        "IpProtocol": "tcp",
                        "ToPort": "3000"
                    }
                ],
                "VpcId": {
                    "Fn::ImportValue": {
                        "Fn::Join": [
                            "-",
                            [
                                {
                                    "Fn::Select": [
                                        0,
                                        {
                                            "Fn::Split": [
                                                "-",
                                                {
                                                    "Ref": "AWS::StackName"
                                                }
                                            ]
                                        }
                                    ]
                                },
                                "cluster-vpc-id"
                            ]
                        ]
                    }
                }
            },
            "Type": "AWS::EC2::SecurityGroup"
        },
        "S3Bucket": {
            "DeletionPolicy": "Retain",
            "Type": "AWS::S3::Bucket"
        },
        "TargetGroup": {
            "DependsOn": "LoadBalancer",
            "Properties": {
                "HealthCheckIntervalSeconds": "20",
                "HealthCheckProtocol": "HTTP",
                "HealthCheckTimeoutSeconds": "15",
                "HealthyThresholdCount": "5",
                "Matcher": {
                    "HttpCode": "200"
                },
                "Port": 3000,
                "Protocol": "HTTP",
                "UnhealthyThresholdCount": "3",
                "VpcId": {
                    "Fn::ImportValue": {
                        "Fn::Join": [
                            "-",
                            [
                                {
                                    "Fn::Select": [
                                        0,
                                        {
                                            "Fn::Split": [
                                                "-",
                                                {
                                                    "Ref": "AWS::StackName"
                                                }
                                            ]
                                        }
                                    ]
                                },
                                "cluster-vpc-id"
                            ]
                        ]
                    }
                }
            },
            "Type": "AWS::ElasticLoadBalancingV2::TargetGroup"
        }
    }
}
