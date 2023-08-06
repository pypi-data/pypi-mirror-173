import uuid
from typing import List, Union

from licenseware.constants.states import States
from licenseware.constants.uploader_types import (
    FileValidationResponse,
    ValidationResponse,
)
from licenseware.constants.web_response import WebResponse
from licenseware.uploader.default_handlers.validators import (
    validate_required_input_type,
    validate_text_contains_any,
)
from licenseware.uploader.validation_parameters import UploaderValidationParameters


def _get_error_message(
    filename_contains_msg: Union[str, bool], filename_endswith_msg: Union[str, bool]
) -> str:

    contains_msg = ""
    if isinstance(filename_contains_msg, str):
        contains_msg = filename_contains_msg

    endswith_msg = ""
    if isinstance(filename_endswith_msg, str):
        endswith_msg = filename_endswith_msg

    return (contains_msg + " " + endswith_msg).strip()


def default_filenames_validation_handler(
    filenames: List[str],
    validation_parameters: UploaderValidationParameters,
    web_response: bool = True,
) -> WebResponse:

    validation_response = []

    if not isinstance(
        validation_parameters, UploaderValidationParameters
    ):  # pragma no cover
        validation_parameters = UploaderValidationParameters(**validation_parameters)

    if validation_parameters.ignore_filenames:
        filenames_ignored = [  # pragma: no cover
            ValidationResponse(
                status=States.SKIPPED,
                filename=filename,
                message=validation_parameters.filename_ignored_message,
            )
            for fn in filenames
            if fn in validation_parameters.ignore_filenames
        ]
        validation_response.extend(filenames_ignored)  # pragma: no cover
        filenames = [
            fn for fn in filenames if fn not in validation_parameters.ignore_filenames
        ]  # pragma: no cover

    for filename in filenames:

        filename_contains_msg = validate_text_contains_any(
            filename,
            validation_parameters.filename_contains,
            regex_escape=validation_parameters.regex_escape,
            raise_error=False,
        )

        filename_endswith_msg = validate_required_input_type(
            filename, validation_parameters.filename_endswith, raise_error=False
        )

        if filename_contains_msg is True and filename_endswith_msg is True:

            validation_response.append(
                ValidationResponse(
                    status=States.SUCCESS,
                    filename=filename,
                    message=validation_parameters.filename_valid_message,
                )
            )

        else:
            validation_response.append(
                ValidationResponse(
                    status=States.FAILED,
                    filename=filename,
                    message=_get_error_message(
                        filename_contains_msg, filename_endswith_msg
                    ),
                )
            )

    filename_response = FileValidationResponse(
        event_id=str(uuid.uuid4()),
        status=States.SUCCESS,
        message="File names were analysed",
        validation=tuple(validation_response),
    )

    if not web_response:
        return filename_response

    return WebResponse(content=filename_response, status_code=200)
