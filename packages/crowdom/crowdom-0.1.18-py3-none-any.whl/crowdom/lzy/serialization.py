import abc
import datetime
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
import json
from typing import Any, Callable, Dict, Generic, List, Optional, Type, TypeVar, Union

from pure_protobuf.dataclasses_ import field, message, one_of, part
from pure_protobuf.oneof import OneOf_
import toloka.client as toloka

from .. import base, classification, classification_loop, client, control, evaluation, objects, pricing, worker
from ..utils import DecimalEncoder

# We use Protobuf to serialize objects on lzy whiteboards.
# Standard pickle serialization does not fit our needs, because in general case refactorings in library code may lead
# to incorrect objects deserialization for old, already persisted whiteboards.
#
# For each class which will be stored in whiteboards, we define its serialization wrapper. A possible alternative is
# to provide additional metadata (@message class decorator, attributes data, etc.) to source classes, but we fully
# separate serialization logic from pure business-logic classes, because:
# 1) Currently we have issues with `pure-protobuf` dependency in Arcadia contrib.
# 2) Some attributes types, i.e. dicts, are not Protobuf serializable, and we don't want to modify source classes only
#    because of serialization needs.
#
# To serialize classes from inheritance schemes, we use Protobuf one_of.
#
# We also have another case, when client defines his own classes. Such sets of classes are limited (i.e. subclasses of
# Class) and we typically know data of these classes (.value for Class inheritor). But we don't know to which class
# we need to deserialize this data. So we introduce classes registry, and the client have to associate a permanent
# name with each of his self-defined class, so we can later instantiate this concrete class by its name.

TolokaObj = toloka.primitives.base.BaseTolokaObject

T = TypeVar('T', bound=Type[Any], covariant=True)
ClassT = TypeVar('ClassT', bound=Type[base.Class], covariant=True)
TolokaObjT = TypeVar('TolokaObjT', bound=Type[TolokaObj], covariant=True)

# DO NOT CHANGE THIS NAMES!
# They are persisted in lzy whiteboards and must remain the same for correct deserialization.
types_registry: Dict[Type[base.Object], str] = {
    base.SbSChoice: 'SbSChoice',
    base.BinaryEvaluation: 'BinaryEvaluation',
    objects.Audio: 'Audio',
    objects.Image: 'Image',
    objects.Text: 'Text',
    objects.Video: 'Video',
}
types_registry_reversed = {name: type for type, name in types_registry.items()}


def register_type(type: Type[base.Object], name: str):
    global types_registry, types_registry_reversed
    types_registry[type] = name
    types_registry_reversed[name] = type


func_registry = {}
func_registry_reversed = {}


def register_func(func: Callable, name: str):
    global func_registry, func_registry_reversed
    func_registry[func] = name
    func_registry_reversed[name] = func


# Most likely we won't need exact version of function as it was implemented at the time of the launch.
# Its outputs will be persisted in whiteboard anyway. So if we can't find it, it's not a problem.
def func_not_found(name: str) -> Callable:
    def f():
        raise RuntimeError(f'function "{name}" not found')

    return f


def load_func(name: str) -> Callable:
    return func_registry_reversed.get(name, func_not_found(name))


def deserialize_one_of_field(field):
    one_of = getattr(field, field.which_one_of)
    if isinstance(one_of, ProtobufSerializer):
        return one_of.deserialize()
    else:
        return one_of  # primitive type


class ProtobufSerializer(Generic[T]):
    @staticmethod
    @abc.abstractmethod
    def serialize(obj: T) -> 'ProtobufSerializer':
        ...

    @abc.abstractmethod
    def deserialize(self) -> T:
        ...


@message
@dataclass
class LocalizedStringEntry:
    lang: str = field(1)
    text: str = field(2)


@message
@dataclass
class LocalizedString(ProtobufSerializer[base.LocalizedString]):
    entries: List[LocalizedStringEntry] = field(1)

    @staticmethod
    def serialize(obj: base.LocalizedString) -> 'LocalizedString':
        return LocalizedString(entries=[LocalizedStringEntry(lang, text) for lang, text in obj.lang_to_text.items()])

    def deserialize(self) -> base.LocalizedString:
        return base.LocalizedString(lang_to_text={entry.lang: entry.text for entry in self.entries})


# For library string enumerations
@message
@dataclass
class StrEnum(ProtobufSerializer[Enum], Generic[ClassT]):
    value: str = field(1)

    @staticmethod
    @abc.abstractmethod
    def enum_cls() -> Type[Enum]:
        ...

    @classmethod
    def serialize(cls, obj: Enum) -> 'StrEnum':
        return cls(value=obj.value)

    def deserialize(self) -> Enum:
        return self.enum_cls()(self.value)


@message
class TextFormat(StrEnum[base.TextFormat]):
    @staticmethod
    def enum_cls() -> Type[base.TextFormat]:
        return base.TextFormat


@message
@dataclass
class Title(ProtobufSerializer[base.Title]):
    text: LocalizedString = field(1)
    format: TextFormat = field(2)

    @staticmethod
    def serialize(obj: base.Title) -> 'Title':
        return Title(text=LocalizedString.serialize(obj.text), format=TextFormat.serialize(obj.format))

    def deserialize(self) -> base.Title:
        return base.Title(text=self.text.deserialize(), format=self.format.deserialize())


@message
class SbSChoice(StrEnum[base.SbSChoice]):
    @staticmethod
    def enum_cls() -> Type[base.SbSChoice]:
        return base.SbSChoice


@message
@dataclass
class BinaryEvaluation(ProtobufSerializer[base.BinaryEvaluation]):
    ok: bool = field(1)

    @staticmethod
    def serialize(obj: base.BinaryEvaluation) -> 'BinaryEvaluation':
        return BinaryEvaluation(obj.ok)

    def deserialize(self) -> base.BinaryEvaluation:
        return base.BinaryEvaluation(self.ok)


@message
@dataclass
class Metadata(ProtobufSerializer[base.Metadata]):
    metadata: str = field(1)

    @staticmethod
    def serialize(obj: base.Metadata) -> 'Metadata':
        return Metadata(obj.metadata)

    def deserialize(self) -> base.Metadata:
        return base.Metadata(self.metadata)


@message
@dataclass
class Text(ProtobufSerializer[objects.Text]):
    text: str = field(1)

    @staticmethod
    def serialize(obj: objects.Text) -> 'Text':
        return Text(obj.text)

    def deserialize(self) -> objects.Text:
        return objects.Text(self.text)


@message
@dataclass
class Audio(ProtobufSerializer[objects.Audio]):
    url: str = field(1)

    @staticmethod
    def serialize(obj: objects.Audio) -> 'Audio':
        return Audio(obj.url)

    def deserialize(self) -> objects.Audio:
        return objects.Audio(self.url)


@message
@dataclass
class Image(ProtobufSerializer[objects.Image]):
    url: str = field(1)

    @staticmethod
    def serialize(obj: objects.Image) -> 'Image':
        return Image(obj.url)

    def deserialize(self) -> objects.Image:
        return objects.Image(self.url)


@message
@dataclass
class Video(ProtobufSerializer[objects.Video]):
    url: str = field(1)

    @staticmethod
    def serialize(obj: objects.Video) -> 'Video':
        return Video(obj.url)

    def deserialize(self) -> objects.Video:
        return objects.Video(self.url)


# For user-defined string enumerations, including Class inheritors
@message
@dataclass
class Class(ProtobufSerializer[base.Class]):
    value: str = field(1)
    cls: str = field(2)

    @staticmethod
    def serialize(obj: base.Class) -> 'Class':
        cls = types_registry[type(obj)]
        return Class(value=obj.value, cls=cls)

    def deserialize(self) -> base.Class:
        cls = types_registry_reversed[self.cls]
        return cls(self.value)


@message
@dataclass
class Label(ProtobufSerializer[base.Label]):
    label: OneOf_ = one_of(
        cls=part(Class, 1),
        sbs_choice=part(SbSChoice, 2),
        binary_evaluation=part(BinaryEvaluation, 3),
    )

    @staticmethod
    def serialize(obj: base.Label) -> 'Label':
        label = Label()
        if isinstance(obj, base.BinaryEvaluation):
            label.label.binary_evaluation = BinaryEvaluation.serialize(obj)
        elif isinstance(obj, base.SbSChoice):
            label.label.sbs_choice = SbSChoice.serialize(obj)
        elif isinstance(obj, base.Class):
            label.label.cls = Class.serialize(obj)
        else:
            assert False, f'unexpected Label type: {type(obj)}'
        return label

    def deserialize(self) -> base.Label:
        return deserialize_one_of_field(self.label)


@message
@dataclass
class Object(ProtobufSerializer[base.Object]):
    obj: OneOf_ = one_of(
        cls=part(Class, 1),
        sbs_choice=part(SbSChoice, 2),
        binary_evaluation=part(BinaryEvaluation, 3),
        metadata=part(Metadata, 4),
        text=part(Text, 5),
        audio=part(Audio, 6),
        image=part(Image, 7),
        video=part(Video, 8),
    )

    @staticmethod
    def serialize(obj: base.Object) -> 'Object':
        obj_ = Object()
        if isinstance(obj, base.BinaryEvaluation):
            obj_.obj.binary_evaluation = BinaryEvaluation.serialize(obj)
        elif isinstance(obj, base.SbSChoice):
            obj_.obj.sbs_choice = SbSChoice.serialize(obj)
        elif isinstance(obj, base.Class):
            obj_.obj.cls = Class.serialize(obj)
        elif isinstance(obj, base.Metadata):
            obj_.obj.metadata = Metadata.serialize(obj)
        elif isinstance(obj, objects.Text):
            obj_.obj.text = Text.serialize(obj)
        elif isinstance(obj, objects.Audio):
            obj_.obj.audio = Audio.serialize(obj)
        elif isinstance(obj, objects.Image):
            obj_.obj.image = Image.serialize(obj)
        elif isinstance(obj, objects.Video):
            obj_.obj.video = Video.serialize(obj)
        else:
            assert False, f'unexpected Object type: {type(obj)}'
        return obj_

    def deserialize(self) -> base.Object:
        return deserialize_one_of_field(self.obj)


@message
@dataclass
class ObjectMeta(ProtobufSerializer[base.ObjectMeta]):
    type: str = field(1)
    name: Optional[str] = field(2, default=None)
    title: Optional[Title] = field(3, default=None)
    required: bool = field(4, default=True)

    @staticmethod
    def serialize(obj: base.ObjectMeta) -> 'ObjectMeta':
        return ObjectMeta(
            type=types_registry[obj.type],
            name=obj.name,
            title=Title.serialize(obj.title) if obj.title else None,
            required=obj.required,
        )

    def deserialize(self) -> base.ObjectMeta:
        return base.ObjectMeta(
            type=types_registry_reversed[self.type],
            name=self.name,
            title=self.title.deserialize() if self.title else None,
            required=self.required,
        )


@message
@dataclass
class AvailableLabels(ProtobufSerializer[base.AvailableLabels]):
    labels: List[Label] = field(1)

    @staticmethod
    def serialize(obj: base.AvailableLabels) -> 'AvailableLabels':
        return AvailableLabels([Label.serialize(label) for label in obj.labels])

    def deserialize(self) -> base.AvailableLabels:
        return base.AvailableLabels([label.deserialize() for label in self.labels])


@message
@dataclass
class Consequence(ProtobufSerializer[base.Consequence]):
    consequence: OneOf_ = one_of(
        available_labels=part(AvailableLabels, 1),
    )

    @staticmethod
    def serialize(obj: base.Consequence) -> 'Consequence':
        consequence = Consequence()
        if isinstance(obj, base.AvailableLabels):
            consequence.consequence.available_labels = AvailableLabels.serialize(obj)
        else:
            raise ValueError(f'unexpected consequence type: {type(obj)}')
        return consequence

    def deserialize(self) -> base.Consequence:
        return deserialize_one_of_field(self.consequence)


@message
@dataclass
class ConditionEquals(ProtobufSerializer[base.ConditionEquals]):
    what: str = field(1)
    to: OneOf_ = one_of(
        str=part(str, 2),
    )

    @staticmethod
    def serialize(obj: base.ConditionEquals) -> 'ConditionEquals':
        condition = ConditionEquals(what=obj.what)
        if isinstance(obj.to, str):
            condition.to.str = obj.to
        else:
            raise ValueError(f'unsupported equals to type: {type(obj.to)}')
        return condition

    def deserialize(self) -> base.ConditionEquals:
        return base.ConditionEquals(what=self.what, to=deserialize_one_of_field(self.to))


@message
@dataclass
class Condition(ProtobufSerializer[base.Condition]):
    condition: OneOf_ = one_of(
        equals=part(ConditionEquals, 1),
    )

    @staticmethod
    def serialize(obj: base.Condition) -> 'Condition':
        condition = Condition()
        if isinstance(obj, base.ConditionEquals):
            condition.condition.equals = ConditionEquals.serialize(obj)
        else:
            raise ValueError(f'unexpected condition type: {type(obj)}')
        return condition

    def deserialize(self) -> base.Condition:
        return deserialize_one_of_field(self.condition)


# then/else branches are originally unions, better option to pack them to one_of, but it's not possible because union
# contains If itself and we can't pass class to one_of part using quotation syntax like 'If'
@dataclass
class If(ProtobufSerializer[base.If]):
    condition: Condition = field(1)
    then_if: Optional['If'] = field(2, default=None)
    then_consequence: Optional[Consequence] = field(3, default=None)
    else_if: Optional['If'] = field(4, default=None)
    else_consequence: Optional[Consequence] = field(5, default=None)

    def __post_init__(self):
        assert (self.then_if is not None) ^ (self.then_consequence is not None)
        assert not (self.else_if is not None and self.else_consequence is not None)

    @staticmethod
    def serialize(obj: base.If) -> 'If':
        return If(
            condition=Condition.serialize(obj.condition),
            then_if=If.serialize(obj.then) if obj.then and isinstance(obj.then, base.If) else None,
            then_consequence=Consequence.serialize(obj.then)
            if obj.then and isinstance(obj.then, base.Consequence)
            else None,
            else_if=If.serialize(obj.else_) if obj.else_ and isinstance(obj.else_, base.If) else None,
            else_consequence=Consequence.serialize(obj.else_)
            if obj.else_ and isinstance(obj.else_, base.Consequence)
            else None,
        )

    def deserialize(self) -> base.If:
        then = self.then_if.deserialize() if self.then_if else self.then_consequence.deserialize()
        else_ = None
        if self.else_if:
            else_ = self.else_if.deserialize()
        if self.else_consequence:
            else_ = self.else_consequence.deserialize()
        return base.If(condition=self.condition.deserialize(), then=then, else_=else_)


# self-referencing classes are decorated with @message separately, see https://github.com/eigenein/protobuf/issues/96
If = message(If)


@message
class LabelsDisplayType(StrEnum[base.LabelsDisplayType]):
    @staticmethod
    def enum_cls() -> Type[base.LabelsDisplayType]:
        return base.LabelsDisplayType


@message
@dataclass
class ClassMeta(ObjectMeta, ProtobufSerializer[base.ClassMeta]):
    available_labels: Optional[If] = field(100, default=None)
    input_display_type: LabelsDisplayType = field(101, default=LabelsDisplayType(base.LabelsDisplayType.MULTI))
    text_format: TextFormat = field(102, default=TextFormat(base.TextFormat.PLAIN))

    @staticmethod
    def serialize(obj: base.ClassMeta) -> 'ClassMeta':
        obj_meta = ObjectMeta.serialize(obj)
        return ClassMeta(
            type=obj_meta.type,
            name=obj_meta.name,
            title=obj_meta.title,
            required=obj_meta.required,
            available_labels=If.serialize(obj.available_labels) if obj.available_labels else None,
            input_display_type=LabelsDisplayType.serialize(obj.input_display_type),
            text_format=TextFormat.serialize(obj.text_format),
        )

    def deserialize(self) -> base.ClassMeta:
        obj_meta = super(ClassMeta, self).deserialize()
        return base.ClassMeta(
            type=obj_meta.type,
            name=obj_meta.name,
            title=obj_meta.title,
            required=obj_meta.required,
            available_labels=self.available_labels.deserialize() if self.available_labels else None,
            input_display_type=self.input_display_type.deserialize(),
            text_format=self.text_format.deserialize(),
        )


@message
@dataclass
class TextValidation(ProtobufSerializer[objects.TextValidation]):
    regex: LocalizedString = field(1)
    hint: LocalizedString = field(2)

    @staticmethod
    def serialize(obj: objects.TextValidation) -> 'TextValidation':
        return TextValidation(
            regex=LocalizedString.serialize(obj.regex),
            hint=LocalizedString.serialize(obj.hint),
        )

    def deserialize(self) -> objects.TextValidation:
        return objects.TextValidation(
            regex=self.regex.deserialize(),
            hint=self.hint.deserialize(),
        )


@message
@dataclass
class TextMeta(ObjectMeta, ProtobufSerializer[objects.TextMeta]):
    format: TextFormat = field(100, default=TextFormat(base.TextFormat.PLAIN))
    validation: Optional[TextValidation] = field(101, default=None)

    @staticmethod
    def serialize(obj: objects.TextMeta) -> 'TextMeta':
        obj_meta = ObjectMeta.serialize(obj)
        return TextMeta(
            type=obj_meta.type,
            name=obj_meta.name,
            title=obj_meta.title,
            required=obj_meta.required,
            format=TextFormat.serialize(obj.format),
            validation=TextValidation.serialize(obj.validation) if obj.validation else None,
        )

    def deserialize(self) -> objects.TextMeta:
        obj_meta = super(TextMeta, self).deserialize()
        return objects.TextMeta(
            type=obj_meta.type,
            name=obj_meta.name,
            title=obj_meta.title,
            required=obj_meta.required,
            format=self.format.deserialize(),
            validation=self.validation.deserialize() if self.validation else None,
        )


@message
@dataclass
class ObjectMetaT(ProtobufSerializer[base.ObjectMeta]):
    meta: OneOf_ = one_of(
        object=part(ObjectMeta, 1),
        cls=part(ClassMeta, 2),
        text=part(TextMeta, 3),
    )

    @staticmethod
    def serialize(obj: base.ObjectMeta) -> 'ObjectMetaT':
        meta = ObjectMetaT()
        if isinstance(obj, base.ClassMeta):
            meta.meta.cls = ClassMeta.serialize(obj)
        elif isinstance(obj, objects.TextMeta):
            meta.meta.text = TextMeta.serialize(obj)
        else:
            meta.meta.object = ObjectMeta.serialize(obj)
        return meta

    def deserialize(self) -> base.ObjectMeta:
        return deserialize_one_of_field(self.meta)


@message
@dataclass
class FunctionArgument(ProtobufSerializer[Union[Type[base.Object], base.ObjectMeta]]):
    arg: OneOf_ = one_of(
        type=part(str, 1),
        meta=part(ObjectMetaT, 2),
    )

    @staticmethod
    def serialize(obj: Union[Type[base.Object], base.ObjectMeta]) -> 'FunctionArgument':
        arg = FunctionArgument()
        if isinstance(obj, base.ObjectMeta):
            arg.arg.meta = ObjectMetaT.serialize(obj)
        else:
            arg.arg.type = types_registry[obj]
        return arg

    def deserialize(self) -> Union[Type[base.Object], base.ObjectMeta]:
        which_one = self.arg.which_one_of
        if which_one == 'type':
            return types_registry_reversed[self.arg.type]
        else:
            return self.arg.meta.deserialize()


@message
@dataclass
class ClassificationFunction(ProtobufSerializer[base.ClassificationFunction]):
    inputs: List[FunctionArgument] = field(1)
    cls: FunctionArgument = field(2)

    @staticmethod
    def serialize(obj: base.ClassificationFunction) -> 'ClassificationFunction':
        return ClassificationFunction(
            inputs=[FunctionArgument.serialize(input) for input in obj.inputs],
            cls=FunctionArgument.serialize(obj.cls),
        )

    def deserialize(self) -> base.ClassificationFunction:
        return base.ClassificationFunction(
            inputs=tuple(FunctionArgument.deserialize(input) for input in self.inputs),
            cls=FunctionArgument.deserialize(self.cls),
        )


sbs_choice = FunctionArgument()
sbs_choice.arg.type = types_registry[base.SbSChoice]


@message
@dataclass
class SbSFunction(ProtobufSerializer[base.SbSFunction]):
    inputs: List[FunctionArgument] = field(1)
    hints: List[FunctionArgument] = field(2, default_factory=list)
    choice: FunctionArgument = field(3, default=sbs_choice)

    @staticmethod
    def serialize(obj: base.SbSFunction) -> 'SbSFunction':
        return SbSFunction(
            inputs=[FunctionArgument.serialize(input) for input in obj.inputs],
            hints=[FunctionArgument.serialize(hint) for hint in obj.hints] if obj.hints else [],
            choice=FunctionArgument.serialize(obj.choice),
        )

    def deserialize(self) -> base.SbSFunction:
        return base.SbSFunction(
            inputs=tuple(FunctionArgument.deserialize(input) for input in self.inputs),
            hints=tuple(FunctionArgument.deserialize(hint) for hint in self.hints) if self.hints else None,
            choice=FunctionArgument.deserialize(self.choice),
        )


@message
@dataclass
class AnnotationFunction(ProtobufSerializer[base.AnnotationFunction]):
    inputs: List[FunctionArgument] = field(1)
    outputs: List[FunctionArgument] = field(2)
    evaluation: FunctionArgument = field(3)

    @staticmethod
    def serialize(obj: base.AnnotationFunction) -> 'AnnotationFunction':
        return AnnotationFunction(
            inputs=[FunctionArgument.serialize(input) for input in obj.inputs],
            outputs=[FunctionArgument.serialize(output) for output in obj.outputs],
            evaluation=FunctionArgument.serialize(obj.evaluation),
        )

    def deserialize(self) -> base.AnnotationFunction:
        return base.AnnotationFunction(
            inputs=tuple(FunctionArgument.deserialize(input) for input in self.inputs),
            outputs=tuple(FunctionArgument.deserialize(output) for output in self.outputs),
            evaluation=FunctionArgument.deserialize(self.evaluation),
        )


@message
@dataclass
class TaskFunction(ProtobufSerializer[base.TaskFunction]):
    function: OneOf_ = one_of(
        classification=part(ClassificationFunction, 1),
        sbs=part(SbSFunction, 2),
        annotation=part(AnnotationFunction, 3),
    )

    @staticmethod
    def serialize(obj: base.TaskFunction) -> 'TaskFunction':
        function = TaskFunction()
        if isinstance(obj, base.ClassificationFunction):
            function.function.classification = ClassificationFunction.serialize(obj)
        elif isinstance(obj, base.SbSFunction):
            function.function.sbs = SbSFunction.serialize(obj)
        elif isinstance(obj, base.AnnotationFunction):
            function.function.annotation = AnnotationFunction.serialize(obj)
        else:
            raise ValueError(f'unexpected function {obj}')
        return function

    def deserialize(self) -> base.TaskFunction:
        return deserialize_one_of_field(self.function)


@message
@dataclass
class TaskSpec(ProtobufSerializer[base.TaskSpec]):
    id: str = field(1)
    function: TaskFunction = field(2)
    name: LocalizedString = field(3)
    description: LocalizedString = field(4)
    instruction: LocalizedString = field(5)

    @staticmethod
    def serialize(obj: base.TaskSpec) -> 'TaskSpec':
        return TaskSpec(
            id=obj.id,
            function=TaskFunction.serialize(obj.function),
            name=LocalizedString.serialize(obj.name),
            description=LocalizedString.serialize(obj.description),
            instruction=LocalizedString.serialize(obj.instruction),
        )

    def deserialize(self) -> base.TaskSpec:
        return base.TaskSpec(
            id=self.id,
            function=self.function.deserialize(),
            name=self.name.deserialize(),
            description=self.description.deserialize(),
            instruction=self.instruction.deserialize(),
        )


@message
class ComparisonType(StrEnum[control.ComparisonType]):
    @staticmethod
    def enum_cls() -> Type[control.ComparisonType]:
        return control.ComparisonType


@message
@dataclass
class PredicateValue(ProtobufSerializer[Union[float, datetime.timedelta]]):
    value: OneOf_ = one_of(
        float_=part(float, 1),
        timedelta=part(datetime.timedelta, 2),
    )

    @staticmethod
    def serialize(obj: Union[float, datetime.timedelta]) -> 'PredicateValue':
        value = PredicateValue()
        if isinstance(obj, datetime.timedelta):
            value.value.timedelta = obj
        else:
            value.value.float_ = obj
        return value

    def deserialize(self) -> Union[float, datetime.timedelta]:
        return deserialize_one_of_field(self.value)


@message
@dataclass
class ThresholdComparisonPredicate(ProtobufSerializer[control.ThresholdComparisonPredicate]):
    threshold: PredicateValue = field(1)
    comparison: ComparisonType = field(2)

    @staticmethod
    def serialize(obj: control.ThresholdComparisonPredicate) -> 'ThresholdComparisonPredicate':
        return ThresholdComparisonPredicate(
            threshold=PredicateValue.serialize(obj.threshold),
            comparison=ComparisonType.serialize(obj.comparison),
        )

    def deserialize(self) -> control.ThresholdComparisonPredicate:
        return control.ThresholdComparisonPredicate(
            threshold=self.threshold.deserialize(),
            comparison=self.comparison.deserialize(),
        )


@message
class BooleanOperator(StrEnum[control.BooleanOperator]):
    @staticmethod
    def enum_cls() -> Type[control.BooleanOperator]:
        return control.BooleanOperator


# better option is to pack predicate types to one_of, but it's not possible because expression predicate
# contains list of Predicates itself, but we can't pass class to one_of part using quotation syntax like 'Predicate'
@dataclass
class Predicate(ProtobufSerializer[control.Predicate]):
    assignment_accuracy: Optional[ThresholdComparisonPredicate] = field(1, default=None)
    assignment_duration: Optional[ThresholdComparisonPredicate] = field(2, default=None)
    always_true: bool = field(3, default=False)
    expression_boolean_operator: Optional[BooleanOperator] = field(4, default=None)
    expression_predicates: List['Predicate'] = field(5, default_factory=list)

    @staticmethod
    def serialize(obj: control.Predicate) -> 'Predicate':
        predicate = Predicate()
        if isinstance(obj, control.AssignmentAccuracyPredicate):
            predicate.assignment_accuracy = ThresholdComparisonPredicate.serialize(obj)
        elif isinstance(obj, control.AssignmentDurationPredicate):
            predicate.assignment_duration = ThresholdComparisonPredicate.serialize(obj)
        elif isinstance(obj, control.AlwaysTruePredicate):
            predicate.always_true = True
        elif isinstance(obj, control.PredicateExpression):
            predicate.expression_boolean_operator = BooleanOperator.serialize(obj.boolean_operator)
            predicate.expression_predicates = [Predicate.serialize(p) for p in obj.predicates]
        else:
            raise ValueError(f'unexpected predicate type: {type(obj)}')
        return predicate

    def deserialize(self) -> control.Predicate:
        threshold_proto = self.assignment_accuracy or self.assignment_duration
        if threshold_proto:
            threshold = ThresholdComparisonPredicate.deserialize(threshold_proto)
            type = (
                control.AssignmentAccuracyPredicate if self.assignment_accuracy else control.AssignmentDurationPredicate
            )
            return type(threshold=threshold.threshold, comparison=threshold.comparison)

        if self.always_true:
            return control.AlwaysTruePredicate()

        assert self.expression_boolean_operator and self.expression_predicates

        return control.PredicateExpression(
            boolean_operator=BooleanOperator.deserialize(self.expression_boolean_operator),
            predicates=[Predicate.deserialize(p) for p in self.expression_predicates],
        )


Predicate = message(Predicate)


@message
@dataclass
class BlockUser(ProtobufSerializer[control.BlockUser]):
    scope: str = field(1)
    private_comment: str = field(2)
    duration: Optional[datetime.timedelta] = field(3, default=None)

    @staticmethod
    def serialize(obj: control.BlockUser) -> 'BlockUser':
        return BlockUser(
            scope=obj.scope.value,
            private_comment=obj.private_comment,
            duration=obj.duration,
        )

    def deserialize(self) -> control.BlockUser:
        return control.BlockUser(
            scope=toloka.user_restriction.UserRestriction.Scope(self.scope),
            private_comment=self.private_comment,
            duration=self.duration,
        )


@message
@dataclass
class GiveBonusToUser(ProtobufSerializer[control.GiveBonusToUser]):
    amount_usd: float = field(1)

    @staticmethod
    def serialize(obj: control.GiveBonusToUser) -> 'GiveBonusToUser':
        return GiveBonusToUser(amount_usd=obj.amount_usd)

    def deserialize(self) -> control.GiveBonusToUser:
        return control.GiveBonusToUser(amount_usd=self.amount_usd)


@message
@dataclass
class SetAssignmentStatus(ProtobufSerializer[control.SetAssignmentStatus]):
    status: str = field(1)

    @staticmethod
    def serialize(obj: control.SetAssignmentStatus) -> 'SetAssignmentStatus':
        return SetAssignmentStatus(status=obj.status.value)

    def deserialize(self) -> control.SetAssignmentStatus:
        return control.SetAssignmentStatus(status=toloka.Assignment.Status(self.status))


@message
@dataclass
class Action(ProtobufSerializer[control.Action]):
    action: OneOf_ = one_of(
        block_user=part(BlockUser, 1),
        give_bonus_to_user=part(GiveBonusToUser, 2),
        set_assignment_status=part(SetAssignmentStatus, 3),
    )

    @staticmethod
    def serialize(obj: control.Action) -> 'Action':
        action = Action()
        if isinstance(obj, control.BlockUser):
            action.action.block_user = BlockUser.serialize(obj)
        elif isinstance(obj, control.GiveBonusToUser):
            action.action.give_bonus_to_user = GiveBonusToUser.serialize(obj)
        elif isinstance(obj, control.SetAssignmentStatus):
            action.action.set_assignment_status = SetAssignmentStatus.serialize(obj)
        else:
            raise ValueError(f'unexpected action type: {type(obj)}')
        return action

    def deserialize(self) -> control.Action:
        return deserialize_one_of_field(self.action)


@message
@dataclass
class Rule(ProtobufSerializer[control.Rule]):
    predicate: Predicate = field(1)
    action: Action = field(2)

    @staticmethod
    def serialize(obj: control.Rule) -> 'Rule':
        return Rule(predicate=Predicate.serialize(obj.predicate), action=Action.serialize(obj.action))

    def deserialize(self) -> control.Rule:
        return control.Rule(predicate=self.predicate.deserialize(), action=self.action.deserialize())


@message
@dataclass
class Control(ProtobufSerializer[control.Control]):
    rules: List[Rule] = field(1, default_factory=list)

    @staticmethod
    def serialize(obj: control.Control) -> 'Control':
        return Control([Rule.serialize(rule) for rule in obj.rules])

    def deserialize(self) -> control.Control:
        return control.Control([rule.deserialize() for rule in self.rules])


@message
@dataclass
class TolokaObject(ProtobufSerializer[TolokaObj], Generic[TolokaObjT]):
    json: str = field(1)

    @classmethod
    def serialize(cls, obj: TolokaObj):
        return cls(json=json.dumps(obj.unstructure(), cls=DecimalEncoder))

    def deserialize(self) -> TolokaObj:
        return self.toloka_cls().structure(json.loads(self.json, parse_float=Decimal))

    @staticmethod
    @abc.abstractmethod
    def toloka_cls() -> Type[TolokaObj]:
        ...


@message
class TolokaPool(TolokaObject[toloka.Pool]):
    @staticmethod
    def toloka_cls() -> Type[TolokaObj]:
        return toloka.Pool


@message
class TolokaFilterCondition(TolokaObject[toloka.filter.FilterCondition]):
    @staticmethod
    def toloka_cls() -> Type[TolokaObj]:
        return toloka.filter.FilterCondition


@message
class TolokaSkill(TolokaObject[toloka.Skill]):
    @staticmethod
    def toloka_cls() -> Type[TolokaObj]:
        return toloka.Skill


@message
@dataclass
class ExpertFilter(ProtobufSerializer[worker.ExpertFilter]):
    skills: List[TolokaSkill] = field(1)

    @staticmethod
    def serialize(obj: worker.ExpertFilter) -> 'ExpertFilter':
        return ExpertFilter([TolokaSkill.serialize(skill) for skill in obj.skills])

    def deserialize(self) -> worker.ExpertFilter:
        return worker.ExpertFilter([skill.deserialize() for skill in self.skills])


@message
@dataclass
class LanguageRequirement(ProtobufSerializer[worker.LanguageRequirement]):
    lang: str = field(1)
    verified: bool = field(2)

    @staticmethod
    def serialize(obj: worker.LanguageRequirement) -> 'LanguageRequirement':
        return LanguageRequirement(lang=obj.lang, verified=obj.verified)

    def deserialize(self) -> worker.LanguageRequirement:
        return worker.LanguageRequirement(lang=self.lang, verified=self.verified)


@message
@dataclass
class BaseWorkerFilter(ProtobufSerializer[worker.BaseWorkerFilter]):
    training_score: Optional[int] = field(1, default=None)

    @staticmethod
    def serialize(obj: worker.BaseWorkerFilter) -> 'BaseWorkerFilter':
        return BaseWorkerFilter(training_score=obj.training_score)

    def deserialize(self) -> worker.BaseWorkerFilter:
        return worker.BaseWorkerFilter(training_score=self.training_score)


@message
@dataclass
class WorkerFilterParams(ProtobufSerializer[worker.WorkerFilter.Params]):
    lang: Optional[LanguageRequirement] = field(1, default=None)
    regions: List[int] = field(2, default_factory=list)
    age_min: Optional[int] = field(3, default=None)
    age_max: Optional[int] = field(4, default=None)
    client_types: List[str] = field(5, default_factory=list)

    @staticmethod
    def serialize(obj: worker.WorkerFilter.Params) -> 'WorkerFilterParams':
        return WorkerFilterParams(
            lang=LanguageRequirement.serialize(obj.lang) if obj.lang else None,
            regions=list(obj.regions),
            age_min=obj.age_range[0],
            age_max=obj.age_range[1],
            client_types=[t.value for t in obj.client_types],
        )

    def deserialize(self) -> worker.WorkerFilter.Params:
        return worker.WorkerFilter.Params(
            lang=self.lang.deserialize() if self.lang else None,
            regions=set(self.regions),
            age_range=(self.age_min, self.age_max),
            client_types={toloka.filter.ClientType.ClientType(t) for t in self.client_types},
        )


@message
@dataclass
class WorkerFilter(BaseWorkerFilter, ProtobufSerializer[worker.WorkerFilter]):
    filters: List[WorkerFilterParams] = field(100, default_factory=list)

    @staticmethod
    def serialize(obj: worker.WorkerFilter) -> 'WorkerFilter':
        base_filter = BaseWorkerFilter.serialize(obj)
        return WorkerFilter(
            training_score=base_filter.training_score, filters=[WorkerFilterParams.serialize(f) for f in obj.filters]
        )

    def deserialize(self) -> worker.WorkerFilter:
        base_filter = super(WorkerFilter, self).deserialize()
        return worker.WorkerFilter(
            training_score=base_filter.training_score,
            filters=[f.deserialize() for f in self.filters],
        )


@message
@dataclass
class CustomWorkerFilter(BaseWorkerFilter, ProtobufSerializer[worker.CustomWorkerFilter]):
    filter: Optional[TolokaFilterCondition] = field(100, default=None)

    @staticmethod
    def serialize(obj: worker.CustomWorkerFilter) -> 'CustomWorkerFilter':
        base_filter = BaseWorkerFilter.serialize(obj)
        return CustomWorkerFilter(
            training_score=base_filter.training_score,
            filter=TolokaFilterCondition.serialize(obj.filter) if obj.filter else None,
        )

    def deserialize(self) -> worker.CustomWorkerFilter:
        base_filter = super(CustomWorkerFilter, self).deserialize()
        return worker.CustomWorkerFilter(
            training_score=base_filter.training_score,
            filter=TolokaFilterCondition.deserialize(self.filter) if self.filter else None,
        )


@message
@dataclass
class HumanFilter(ProtobufSerializer[worker.HumanFilter]):
    filter: OneOf_ = one_of(
        expert=part(ExpertFilter, 1),
        worker=part(WorkerFilter, 2),
        custom_worker=part(CustomWorkerFilter, 3),
    )

    @staticmethod
    def serialize(obj: worker.HumanFilter) -> 'HumanFilter':
        f = HumanFilter()
        if isinstance(obj, worker.ExpertFilter):
            f.filter.expert = ExpertFilter.serialize(obj)
        elif isinstance(obj, worker.WorkerFilter):
            f.filter.worker = WorkerFilter.serialize(obj)
        elif isinstance(obj, worker.CustomWorkerFilter):
            f.filter.custom_worker = CustomWorkerFilter.serialize(obj)
        else:
            raise ValueError(f'unexpected filter type: {type(obj)}')
        return f

    def deserialize(self) -> worker.HumanFilter:
        return deserialize_one_of_field(self.filter)


@message
@dataclass
class StaticPricingStrategy(ProtobufSerializer[pricing.StaticPricingStrategy]):
    @staticmethod
    def serialize(obj: pricing.StaticPricingStrategy) -> 'StaticPricingStrategy':
        return StaticPricingStrategy()

    def deserialize(self) -> pricing.StaticPricingStrategy:
        return pricing.StaticPricingStrategy()


@message
@dataclass
class DynamicPricingStrategy(ProtobufSerializer[pricing.DynamicPricingStrategy]):
    max_ratio: float = field(1)

    @staticmethod
    def serialize(obj: pricing.DynamicPricingStrategy) -> 'DynamicPricingStrategy':
        return DynamicPricingStrategy(obj.max_ratio)

    def deserialize(self) -> pricing.DynamicPricingStrategy:
        return pricing.DynamicPricingStrategy(self.max_ratio)


@message
@dataclass
class PricingStrategy(ProtobufSerializer[pricing.PricingStrategy]):
    strategy: OneOf_ = one_of(
        static=part(StaticPricingStrategy, 1),
        dynamic=part(DynamicPricingStrategy, 2),
    )

    @staticmethod
    def serialize(obj: pricing.PricingStrategy) -> 'PricingStrategy':
        strategy = PricingStrategy()
        if isinstance(obj, pricing.StaticPricingStrategy):
            strategy.strategy.static = StaticPricingStrategy.serialize(obj)
        elif isinstance(obj, pricing.DynamicPricingStrategy):
            strategy.strategy.dynamic = DynamicPricingStrategy.serialize(obj)
        else:
            raise ValueError(f'unexpected pricing strategy type: {type(obj)}')
        return strategy

    def deserialize(self) -> pricing.PricingStrategy:
        return deserialize_one_of_field(self.strategy)


@message
@dataclass
class Human(ProtobufSerializer[worker.Human]):
    user_id: str = field(1)
    assignment_id: str = field(2)

    @staticmethod
    def serialize(obj: worker.Human) -> 'Human':
        return Human(user_id=obj.user_id, assignment_id=obj.assignment_id)

    def deserialize(self) -> worker.Human:
        fake_assignment = toloka.Assignment(id=self.assignment_id, user_id=self.user_id)  # TODO: ugly hack
        return worker.Human(fake_assignment)


@message
@dataclass
class Model(ProtobufSerializer[worker.Model]):
    name: str = field(1)
    func: str = field(2)

    @staticmethod
    def serialize(obj: worker.Model) -> 'Model':
        return Model(name=obj.name, func=func_registry[obj.func])

    def deserialize(self) -> worker.Model:
        return worker.Model(name=self.name, func=load_func(self.func))


@message
@dataclass
class Worker(ProtobufSerializer[worker.Worker]):
    worker: OneOf_ = one_of(
        human=part(Human, 1),
        model=part(Model, 2),
    )

    @staticmethod
    def serialize(obj: T) -> 'Worker':
        w = Worker()
        if isinstance(obj, worker.Human):
            w.worker.human = Human.serialize(obj)
        elif isinstance(obj, worker.Model):
            w.worker.model = Model.serialize(obj)
        else:
            raise ValueError(f'unexpected worker type: {type(obj)}')
        return w

    def deserialize(self) -> T:
        return deserialize_one_of_field(self.worker)


@message
@dataclass
class LabelProba(ProtobufSerializer[classification.LabelProba]):
    label: Label = field(1)
    proba: float = field(2)

    @staticmethod
    def serialize(obj: classification.LabelProba) -> 'LabelProba':
        label, proba = obj
        return LabelProba(label=Label.serialize(label), proba=proba)

    def deserialize(self) -> classification.LabelProba:
        return self.label.deserialize(), self.proba


@message
@dataclass
class TaskLabelsProbas(ProtobufSerializer[classification.TaskLabelsProbas]):
    items: List[LabelProba] = field(1, default_factory=list)

    @staticmethod
    def serialize(obj: classification.TaskLabelsProbas) -> 'TaskLabelsProbas':
        return TaskLabelsProbas(items=[LabelProba.serialize((label, proba)) for label, proba in obj.items()])

    def deserialize(self) -> classification.TaskLabelsProbas:
        return {item.label.deserialize(): item.proba for item in self.items}


@message
@dataclass
class StaticOverlap(ProtobufSerializer[classification_loop.StaticOverlap]):
    overlap: int = field(1)

    @staticmethod
    def serialize(obj: classification_loop.StaticOverlap) -> 'StaticOverlap':
        return StaticOverlap(overlap=obj.overlap)

    def deserialize(self) -> classification_loop.StaticOverlap:
        return classification_loop.StaticOverlap(overlap=self.overlap)


@message
@dataclass
class DynamicOverlap(ProtobufSerializer[classification_loop.DynamicOverlap]):
    min_overlap: int = field(1)
    max_overlap: int = field(2)
    confidence: OneOf_ = one_of(
        unified=part(float, 3),
        per_label=part(TaskLabelsProbas, 4),
    )

    @staticmethod
    def serialize(obj: classification_loop.DynamicOverlap) -> 'DynamicOverlap':
        overlap = DynamicOverlap(min_overlap=obj.min_overlap, max_overlap=obj.max_overlap)
        if isinstance(obj.confidence, float):
            overlap.confidence.unified = obj.confidence
        elif isinstance(obj.confidence, dict):
            overlap.confidence.per_label = TaskLabelsProbas.serialize(obj.confidence)
        else:
            raise ValueError(f'unexpected confidence type: {type(obj.confidence)}')
        return overlap

    def deserialize(self) -> classification_loop.DynamicOverlap:
        return classification_loop.DynamicOverlap(
            min_overlap=self.min_overlap,
            max_overlap=self.max_overlap,
            confidence=deserialize_one_of_field(self.confidence),
        )


@message
@dataclass
class Overlap(ProtobufSerializer[classification_loop.Overlap]):
    overlap: OneOf_ = one_of(
        static=part(StaticOverlap, 1),
        dynamic=part(DynamicOverlap, 2),
    )

    @staticmethod
    def serialize(obj: classification_loop.Overlap) -> 'Overlap':
        overlap = Overlap()
        if isinstance(obj, classification_loop.StaticOverlap):
            overlap.overlap.static = StaticOverlap.serialize(obj)
        elif isinstance(obj, classification_loop.DynamicOverlap):
            overlap.overlap.dynamic = DynamicOverlap.serialize(obj)
        else:
            raise ValueError(f'unexpected overlap type: {type(obj)}')
        return overlap

    def deserialize(self) -> classification_loop.Overlap:
        return deserialize_one_of_field(self.overlap)


@message
class AggregationAlgorithm(StrEnum[classification.AggregationAlgorithm]):
    @staticmethod
    def enum_cls() -> Type[classification.AggregationAlgorithm]:
        return classification.AggregationAlgorithm


@message
@dataclass
class ExpertParams(ProtobufSerializer[client.ExpertParams]):
    task_duration_hint: datetime.timedelta = field(1)
    assignment_price: float = field(2)
    real_tasks_count: int = field(3)

    @staticmethod
    def serialize(obj: client.ExpertParams) -> 'ExpertParams':
        return ExpertParams(
            task_duration_hint=obj.task_duration_hint,
            assignment_price=obj.assignment_price,
            real_tasks_count=obj.real_tasks_count,
        )

    def deserialize(self) -> client.ExpertParams:
        return client.ExpertParams(
            task_duration_hint=self.task_duration_hint,
            pricing_config=pricing.PoolPricingConfig(
                assignment_price=self.assignment_price,
                real_tasks_count=self.real_tasks_count,
                control_tasks_count=0,
            ),
        )


@message
@dataclass
class Params(ExpertParams, ProtobufSerializer[client.Params]):
    worker_filter: HumanFilter = field(100)
    control_tasks_count: int = field(101)
    pricing_strategy: PricingStrategy = field(102)
    control: Control = field(103)
    overlap: Overlap = field(104)
    aggregation_algorithm: Optional[AggregationAlgorithm] = field(105, default=None)
    model: Optional[Model] = field(106, default=None)
    task_duration_function: Optional[str] = field(107, default=None)

    @staticmethod
    def serialize(obj: client.Params) -> 'Params':
        expert_params = ExpertParams.serialize(obj)
        return Params(
            task_duration_hint=expert_params.task_duration_hint,
            assignment_price=expert_params.assignment_price,
            real_tasks_count=expert_params.real_tasks_count,
            worker_filter=HumanFilter.serialize(obj.worker_filter),
            control_tasks_count=obj.control_tasks_count,
            pricing_strategy=PricingStrategy.serialize(obj.pricing_strategy),
            control=Control.serialize(obj.control),
            overlap=Overlap.serialize(obj.overlap),
            aggregation_algorithm=AggregationAlgorithm.serialize(obj.aggregation_algorithm)
            if obj.aggregation_algorithm
            else None,
            model=Model.serialize(obj.model) if obj.model else None,
            task_duration_function=func_registry[obj.task_duration_function] if obj.task_duration_function else None,
        )

    def deserialize(self) -> client.Params:
        expert_params = super(Params, self).deserialize()
        return client.Params(
            task_duration_hint=expert_params.task_duration_hint,
            pricing_config=pricing.PoolPricingConfig(
                assignment_price=expert_params.pricing_config.assignment_price,
                real_tasks_count=expert_params.pricing_config.real_tasks_count,
                control_tasks_count=self.control_tasks_count,
            ),
            overlap=Overlap.deserialize(self.overlap),
            control=Control.deserialize(self.control),
            worker_filter=HumanFilter.deserialize(self.worker_filter),
            aggregation_algorithm=AggregationAlgorithm.deserialize(self.aggregation_algorithm)
            if self.aggregation_algorithm
            else None,
            pricing_strategy=PricingStrategy.deserialize(self.pricing_strategy),
            task_duration_function=func_registry_reversed[self.task_duration_function]
            if self.task_duration_function
            else None,
        )


@message
@dataclass
class AssignmentCheckSample(ProtobufSerializer[evaluation.AssignmentCheckSample]):
    max_tasks_to_check: Optional[int] = field(1, default=None)
    assignment_accuracy_finalization_threshold: Optional[float] = field(2, default=None)

    @staticmethod
    def serialize(obj: evaluation.AssignmentCheckSample) -> 'AssignmentCheckSample':
        return AssignmentCheckSample(
            max_tasks_to_check=obj.max_tasks_to_check,
            assignment_accuracy_finalization_threshold=obj.assignment_accuracy_finalization_threshold,
        )

    def deserialize(self) -> evaluation.AssignmentCheckSample:
        return evaluation.AssignmentCheckSample(
            max_tasks_to_check=self.max_tasks_to_check,
            assignment_accuracy_finalization_threshold=self.assignment_accuracy_finalization_threshold,
        )


@message
@dataclass
class AnnotationParams(Params, ProtobufSerializer[client.AnnotationParams]):
    assignment_check_sample: Optional[AssignmentCheckSample] = field(200, default=None)

    @staticmethod
    def serialize(obj: client.AnnotationParams) -> 'AnnotationParams':
        params = Params.serialize(obj)
        return AnnotationParams(
            task_duration_hint=params.task_duration_hint,
            assignment_price=params.assignment_price,
            real_tasks_count=params.real_tasks_count,
            worker_filter=params.worker_filter,
            control_tasks_count=params.control_tasks_count,
            pricing_strategy=params.pricing_strategy,
            control=params.control,
            overlap=params.overlap,
            aggregation_algorithm=params.aggregation_algorithm,
            model=params.model,
            task_duration_function=params.task_duration_function,
            assignment_check_sample=AssignmentCheckSample.serialize(obj.assignment_check_sample)
            if obj.assignment_check_sample
            else None,
        )

    def deserialize(self) -> client.AnnotationParams:
        params = super(AnnotationParams, self).deserialize()
        annotation_params = client.AnnotationParams(
            task_duration_hint=params.task_duration_hint,
            pricing_config=params.pricing_config,
            overlap=params.overlap,
            control=params.control,
            worker_filter=params.worker_filter,
            aggregation_algorithm=params.aggregation_algorithm,
            pricing_strategy=params.pricing_strategy,
            task_duration_function=params.task_duration_function,
            assignment_check_sample=self.assignment_check_sample.deserialize()
            if self.assignment_check_sample
            else None,
        )
        if self.model:
            annotation_params.model = Model.deserialize(self.model)
        return annotation_params
