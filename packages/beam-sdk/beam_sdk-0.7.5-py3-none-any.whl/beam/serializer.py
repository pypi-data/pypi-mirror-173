from marshmallow import Schema, fields, validate, ValidationError
from beam.exceptions import BeamSerializationError
from beam.types import PythonVersion


class BaseSerializer(Schema):
    def validate_and_dump(self, data):
        validation_errors = self.validate(data)

        if len(validation_errors) > 0:
            raise BeamSerializationError(
                f"{self.__class__.__name__}\n{validation_errors}"
            )
        return self.dump(dict)

    def validate(self, data, raise_exception=False, **kwargs):
        if raise_exception:
            validation_errors = self.validate(data)

            if len(validation_errors) > 0:
                raise BeamSerializationError(
                    f"{self.__class__.__name__}\n{validation_errors}"
                )
        return super().validate(data, **kwargs)

    class Meta:
        ordered = True


class AppSpecConfigurationSerializer(BaseSerializer):
    name = fields.String(required=True, validate=validate.Length(max=128))
    cpu = fields.String(required=True)
    gpu = fields.Integer(required=True)
    memory = fields.String(required=True)
    apt_install = fields.List(fields.String(), required=True)
    python_version = fields.String(
        validate=validate.OneOf(
            choices=[version[1] for version in PythonVersion.Types]
        ),
        required=True,
    )
    python_packages = fields.List(fields.String(), required=True)
    workspace = fields.String(required=True)


class BaseTriggerSerializer(BaseSerializer):
    inputs = fields.Dict(
        keys=fields.String(),
        values=fields.Dict(),
    )
    outputs = fields.Dict(
        keys=fields.String(),
        values=fields.Dict(),
    )
    handler = fields.Method(deserialize="validate_handler")
    trigger_type = fields.String()

    def raise_handler_validation_error(self):
        raise ValidationError("must be a string in form {pathToFile}:{method}")

    def validate_handler(self, handler):
        if not isinstance(handler, str):
            self.raise_handler_validation_error()

        parsed_handler = handler.split(":")

        if len(parsed_handler) != 2:
            self.raise_handler_validation_error()


class CronJobTriggerSerializer(BaseTriggerSerializer):
    # TODO: Validation step needs to be handled somewhere
    cron_schedule = fields.String()
