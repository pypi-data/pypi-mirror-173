from typing import Any, List

try:
    # This works on MacOS but not Ubuntu
    from markdowntable import markdownTable  # type: ignore
except:
    # This works on Ubuntu but not MacOS
    from markdownTable import markdownTable  # type: ignore

from pydantic import BaseModel

from py2tf.converters.jinja import JinjaConverter


class MarkdownTableBuilder(markdownTable):
    def getHeader(self):
        # The only change in this function from the parent is the `title` casing
        header = ""
        if self.row_sep in ("topbottom", "always"):
            header += self.newline_char + self.var_row_sep_last + self.newline_char
        for key in self.data[0].keys():
            margin = self.var_padding[key] - len(key)
            right = self.getMargin(margin)
            header += "|" + key.title().rjust(self.var_padding[key] - right, self.padding_char).ljust(
                self.var_padding[key], self.padding_char
            )
        header += "|" + self.newline_char
        if self.row_sep == "always":
            header += self.var_row_sep + self.newline_char
        if self.row_sep == "markdown":
            header += self.var_row_sep.replace("+", "|") + self.newline_char
        return header


class MarkdownConverter(JinjaConverter):

    numbers: List[str] = []  # ["int", "float", "integer"]
    objects: List[str] = ["dict", "object"]
    pass_through_fields: List[str] = ["string", "int", "float", "integer"]

    def __init__(self, format="table") -> None:
        self.format = format

    def convert(self, model: BaseModel) -> str:

        schema = model.schema()
        output = ""
        fields = []
        for field_name, field_data in schema["properties"].items():
            if field_name == "type":
                continue
            fields.append(self.convert_field(schema, field_name, field_data))

        # Sort required fields to the top, then sort by alphabet.
        fields.sort(key=lambda t: (0 if t["Required"] == "Yes" else 1, t["Name"]))

        return MarkdownTableBuilder(fields).setParams(quote=False, row_sep="markdown").getMarkdown()

    def convert_field(self, schema, field_name, field_data) -> Any:
        field_data = self.get_field_data(schema, field_name, field_data)
        description = ""
        if "description" in field_data and field_data["description"]:
            description = field_data["description"]

        return {
            "Name": f"`{field_name}`",
            "Type": field_data.get("type", ""),
            "Description": description,
            "Default": field_data["default"] if field_data["has_default"] else "",
            "Required": "Yes" if field_data["required"] else "No",
        }

    def get_type(self, field_name, field_data):
        type, validators = super(MarkdownConverter, self).get_type(field_name, field_data)
        if type == "bool":
            type = "boolean"
        if "list" in type:
            type = type.replace("list", "array")
        return type, validators
