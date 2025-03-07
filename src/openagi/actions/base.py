from textwrap import dedent
from pydantic import BaseModel, Field
from typing import Any, Optional

from openagi.llms.base import LLMBaseModel
from openagi.memory.memory import Memory
from typing import ClassVar, Dict, Any

class BaseAction(BaseModel):
    """Base Actions class to be inherited by other actions, providing basic functionality and structure."""

    session_id: int = Field(default_factory=str, description="SessionID of the current run.")
    previous_action: Optional[Any] = Field(
        default=None,
        description="Observation or Result of the previous action that might needed to run the current action.",
    )
    llm: Optional[LLMBaseModel] = Field(
        description="LLM Model to be used.", default=None, exclude=True
    )
    memory: Optional[Memory] = Field(
        description="Memory that stores the results of the earlier tasks executed for the current objective.",
        exclude=True,
        default=None,
    )

    def execute(self):
        """Executes the action"""
        raise NotImplementedError("Subclasses must implement this method.")

    @classmethod
    def cls_doc(cls):
        default_exclude_doc_fields = ["llm", "memory", "session_id", "name", "description"]
        return {
            "cls": {
                "kls": cls.__name__,
                "module": cls.__module__,
                "doc": dedent(cls.__doc__).strip() if cls.__doc__ else "",
            },
            "params": {
                field_name: field.description
                for field_name, field in cls.model_fields.items()
                if field_name not in default_exclude_doc_fields
            },
        }

class ConfigurableAction(BaseAction):
    config: ClassVar[Dict[str, Any]] = {}

    @classmethod
    def set_config(cls, *args, **kwargs):
        if args:
            if len(args) == 1 and isinstance(args[0], dict):
                cls.config.update(args[0])
            else:
                raise ValueError("If using positional arguments, a single dictionary must be provided.")
        cls.config.update(kwargs)

    @classmethod
    def get_config(cls, key: str, default: Any = None) -> Any:
        return cls.config.get(key, default)