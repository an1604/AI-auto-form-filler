from pydantic import BaseModel, Field
from typing import Optional, List, Union


class FormField(BaseModel):
    name: Optional[str] = Field(description="The name of the form field.")
    type: Optional[str] = Field(description="The type of the form field (e.g., text, email, file, etc.).")
    id: Optional[str] = Field(description="The unique identifier of the form field, if available.")
    class_name: Optional[List[str]] = Field(alias="class",
                                            description="The class names applied to the field, if available.")
    label: Optional[str] = Field(description="The label associated with the field, if available.")
    value: Optional[str] = Field(description="The current value of the field.")
    placeholder: Optional[str] = Field(description="The placeholder text for the field, if available.")


class SubmitButton(BaseModel):
    text: Optional[str] = Field(description="The text displayed on the submit button, which may be empty.")
    id: Optional[str] = Field(description="The unique identifier of the submit button, if available.")
    class_name: Optional[List[str]] = Field(alias="class",
                                            description="The class names applied to the button, if available.")


class Form(BaseModel):
    action: Optional[str] = Field(description="The action URL where the form is submitted.")
    method: Optional[str] = Field(description="The HTTP method used by the form (e.g., GET, POST).")
    fields: List[FormField] = Field(description="A list of form fields.")
    submit_buttons: List[SubmitButton] = Field(description="A list of submit buttons associated with the form.")


class FormScraper(BaseModel):
    forms: List[Form] = Field(description="A list of all forms identified in the HTML content.")
