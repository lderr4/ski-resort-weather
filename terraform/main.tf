# aws_db_instance.rds:
resource "aws_db_instance" "rds" {
    allocated_storage                     = 20
    auto_minor_version_upgrade            = true
    availability_zone                     = "us-east-1c"
    backup_retention_period               = 1
    backup_target                         = "region"
    backup_window                         = "08:44-09:14"
    ca_cert_identifier                    = "rds-ca-rsa2048-g1"
    copy_tags_to_snapshot                 = true
    customer_owned_ip_enabled             = false
    db_subnet_group_name                  = "default-vpc-083756c4bdcfe481b"
    dedicated_log_volume                  = false
    delete_automated_backups              = true
    deletion_protection                   = false
    enabled_cloudwatch_logs_exports       = []
    engine                                = "postgres"
    engine_lifecycle_support              = "open-source-rds-extended-support-disabled"
    engine_version                        = "16.3"
    iam_database_authentication_enabled   = false
    identifier                            = "database-1"
    instance_class                        = "db.t4g.micro"
    iops                                  = 0
    kms_key_id                            = "arn:aws:kms:us-east-1:207567776666:key/ee918943-f87e-4901-bf77-3ecda890e2c9"
    license_model                         = "postgresql-license"
    maintenance_window                    = "fri:03:53-fri:04:23"
    max_allocated_storage                 = 0
    monitoring_interval                   = 0
    multi_az                              = false
    network_type                          = "IPV4"
    option_group_name                     = "default:postgres-16"
    parameter_group_name                  = "default.postgres16"
    performance_insights_enabled          = true
    performance_insights_kms_key_id       = "arn:aws:kms:us-east-1:207567776666:key/ee918943-f87e-4901-bf77-3ecda890e2c9"
    performance_insights_retention_period = 7
    port                                  = 5432
    publicly_accessible                   = false
    skip_final_snapshot                   = true
    storage_encrypted                     = true
    storage_throughput                    = 0
    storage_type                          = "gp2"
    tags                                  = {}
    tags_all                              = {}
    username                              = "postgres"
    vpc_security_group_ids                = [
        "sg-0b28b141d748ea0a3",
    ]
}

resource "aws_instance" "ec2" {
    ami                                  = "ami-05b10e08d247fb927"
    instance_type                        = "t3a.medium"
    associate_public_ip_address          = true
    availability_zone                    = "us-east-1c"
    disable_api_termination              = false
    ebs_optimized                        = true
    hibernation                          = false
    instance_initiated_shutdown_behavior = "stop"
    key_name                             = "final_key"
    monitoring                           = false
    security_groups                      = [
        "ec2-rds-1",
        "launch-wizard-3",
    ]
    subnet_id                            = "subnet-03d2e414cb8018e78"
    tags                                 = {
        "Name" = "ski-resort-weather"
    }
    vpc_security_group_ids               = [
        "sg-055d26924dd66b1b6",
        "sg-0995a41c59e3f641c",
    ]

    root_block_device {
        delete_on_termination = true
        encrypted             = false
        iops                  = 3000
        throughput            = 125
        volume_size           = 8
        volume_type           = "gp3"
    }

    metadata_options {
        http_endpoint               = "enabled"
        http_put_response_hop_limit = 2
        http_tokens                 = "required"
        instance_metadata_tags      = "disabled"
    }

    credit_specification {
        cpu_credits = "unlimited"
    }
}