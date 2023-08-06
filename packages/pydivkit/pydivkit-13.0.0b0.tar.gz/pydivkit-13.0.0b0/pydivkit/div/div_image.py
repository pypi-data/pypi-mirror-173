# Generated code. Do not modify.
# flake8: noqa: F401, F405, F811

from __future__ import annotations

import enum
import typing

from pydivkit.core import BaseDiv, Field

from . import (
    div_accessibility, div_action, div_alignment_horizontal,
    div_alignment_vertical, div_animation, div_appearance_transition,
    div_aspect, div_background, div_blend_mode, div_border,
    div_change_transition, div_edge_insets, div_extension, div_fade_transition,
    div_focus, div_image_scale, div_size, div_tooltip, div_transform,
    div_transition_trigger, div_visibility, div_visibility_action,
)


# Image.
class DivImage(BaseDiv):

    def __init__(
        self, *,
        image_url: str,
        type: str = "image",
        accessibility: typing.Optional[div_accessibility.DivAccessibility] = None,
        action: typing.Optional[div_action.DivAction] = None,
        action_animation: typing.Optional[div_animation.DivAnimation] = None,
        actions: typing.Optional[typing.List[div_action.DivAction]] = None,
        alignment_horizontal: typing.Optional[div_alignment_horizontal.DivAlignmentHorizontal] = None,
        alignment_vertical: typing.Optional[div_alignment_vertical.DivAlignmentVertical] = None,
        alpha: typing.Optional[float] = None,
        appearance_animation: typing.Optional[div_fade_transition.DivFadeTransition] = None,
        aspect: typing.Optional[div_aspect.DivAspect] = None,
        background: typing.Optional[typing.List[div_background.DivBackground]] = None,
        border: typing.Optional[div_border.DivBorder] = None,
        column_span: typing.Optional[int] = None,
        content_alignment_horizontal: typing.Optional[div_alignment_horizontal.DivAlignmentHorizontal] = None,
        content_alignment_vertical: typing.Optional[div_alignment_vertical.DivAlignmentVertical] = None,
        doubletap_actions: typing.Optional[typing.List[div_action.DivAction]] = None,
        extensions: typing.Optional[typing.List[div_extension.DivExtension]] = None,
        focus: typing.Optional[div_focus.DivFocus] = None,
        height: typing.Optional[div_size.DivSize] = None,
        high_priority_preview_show: typing.Optional[bool] = None,
        id: typing.Optional[str] = None,
        longtap_actions: typing.Optional[typing.List[div_action.DivAction]] = None,
        margins: typing.Optional[div_edge_insets.DivEdgeInsets] = None,
        paddings: typing.Optional[div_edge_insets.DivEdgeInsets] = None,
        placeholder_color: typing.Optional[str] = None,
        preload_required: typing.Optional[bool] = None,
        preview: typing.Optional[str] = None,
        row_span: typing.Optional[int] = None,
        scale: typing.Optional[div_image_scale.DivImageScale] = None,
        selected_actions: typing.Optional[typing.List[div_action.DivAction]] = None,
        tint_color: typing.Optional[str] = None,
        tint_mode: typing.Optional[div_blend_mode.DivBlendMode] = None,
        tooltips: typing.Optional[typing.List[div_tooltip.DivTooltip]] = None,
        transform: typing.Optional[div_transform.DivTransform] = None,
        transition_change: typing.Optional[div_change_transition.DivChangeTransition] = None,
        transition_in: typing.Optional[div_appearance_transition.DivAppearanceTransition] = None,
        transition_out: typing.Optional[div_appearance_transition.DivAppearanceTransition] = None,
        transition_triggers: typing.Optional[typing.List[div_transition_trigger.DivTransitionTrigger]] = None,
        visibility: typing.Optional[div_visibility.DivVisibility] = None,
        visibility_action: typing.Optional[div_visibility_action.DivVisibilityAction] = None,
        visibility_actions: typing.Optional[typing.List[div_visibility_action.DivVisibilityAction]] = None,
        width: typing.Optional[div_size.DivSize] = None,
    ):
        super().__init__(
            type=type,
            accessibility=accessibility,
            action=action,
            action_animation=action_animation,
            actions=actions,
            alignment_horizontal=alignment_horizontal,
            alignment_vertical=alignment_vertical,
            alpha=alpha,
            appearance_animation=appearance_animation,
            aspect=aspect,
            background=background,
            border=border,
            column_span=column_span,
            content_alignment_horizontal=content_alignment_horizontal,
            content_alignment_vertical=content_alignment_vertical,
            doubletap_actions=doubletap_actions,
            extensions=extensions,
            focus=focus,
            height=height,
            high_priority_preview_show=high_priority_preview_show,
            id=id,
            image_url=image_url,
            longtap_actions=longtap_actions,
            margins=margins,
            paddings=paddings,
            placeholder_color=placeholder_color,
            preload_required=preload_required,
            preview=preview,
            row_span=row_span,
            scale=scale,
            selected_actions=selected_actions,
            tint_color=tint_color,
            tint_mode=tint_mode,
            tooltips=tooltips,
            transform=transform,
            transition_change=transition_change,
            transition_in=transition_in,
            transition_out=transition_out,
            transition_triggers=transition_triggers,
            visibility=visibility,
            visibility_action=visibility_action,
            visibility_actions=visibility_actions,
            width=width,
        )

    type: str = Field(default="image")
    accessibility: typing.Optional[div_accessibility.DivAccessibility] = Field(
        description="Accessibility for disabled people.",
    )
    action: typing.Optional[div_action.DivAction] = Field(
        description=(
            "One action when clicking on an element. Not used if the "
            "`actions` parameter isset."
        ),
    )
    action_animation: typing.Optional[div_animation.DivAnimation] = Field(
        description=(
            "Action animation. Web supports `fade`, `scale` and `set` "
            "only."
        ),
    )
    actions: typing.Optional[typing.List[div_action.DivAction]] = Field(
        min_items=1, 
        description="Multiple actions when clicking on an element.",
    )
    alignment_horizontal: typing.Optional[div_alignment_horizontal.DivAlignmentHorizontal] = Field(
        description=(
            "Horizontal alignment of an element inside the parent "
            "element."
        ),
    )
    alignment_vertical: typing.Optional[div_alignment_vertical.DivAlignmentVertical] = Field(
        description=(
            "Vertical alignment of an element inside the parent element."
        ),
    )
    alpha: typing.Optional[float] = Field(
        description=(
            "Sets transparency of the entire element: `0` — completely "
            "transparent, `1` —opaque."
        ),
    )
    appearance_animation: typing.Optional[div_fade_transition.DivFadeTransition] = Field(
        description="Transparency animation when loading an image.",
    )
    aspect: typing.Optional[div_aspect.DivAspect] = Field(
    )
    background: typing.Optional[typing.List[div_background.DivBackground]] = Field(
        min_items=1, 
        description="Element background. It can contain multiple layers.",
    )
    border: typing.Optional[div_border.DivBorder] = Field(
        description="Element stroke.",
    )
    column_span: typing.Optional[int] = Field(
        description=(
            "Merges cells in a column of the [grid](div-grid.md) "
            "element."
        ),
    )
    content_alignment_horizontal: typing.Optional[div_alignment_horizontal.DivAlignmentHorizontal] = Field(
        description="Horizontal image alignment.",
    )
    content_alignment_vertical: typing.Optional[div_alignment_vertical.DivAlignmentVertical] = Field(
        description="Vertical image alignment.",
    )
    doubletap_actions: typing.Optional[typing.List[div_action.DivAction]] = Field(
        min_items=1, 
        description="Action when double-clicking on an element.",
    )
    extensions: typing.Optional[typing.List[div_extension.DivExtension]] = Field(
        min_items=1, 
        description=(
            "Extensions for additional processing of an element. The "
            "list of extensions isgiven in "
            "[DivExtension](../../extensions.dita)."
        ),
    )
    focus: typing.Optional[div_focus.DivFocus] = Field(
        description="Parameters when focusing on an element or losing focus.",
    )
    height: typing.Optional[div_size.DivSize] = Field(
        description=(
            "Element height. For Android: if there is text in this or in "
            "a child element,specify height in `sp` to scale the element "
            "together with the text. To learn moreabout units of size "
            "measurement, see [Layout inside the "
            "card](../../layout.dita)."
        ),
    )
    high_priority_preview_show: typing.Optional[bool] = Field(
        description=(
            "It sets the priority of displaying the preview — the "
            "preview is decoded in themain stream and displayed as the "
            "first frame. Use the parameter carefully — itwill worsen "
            "the preview display time and can worsen the application "
            "launch time."
        ),
    )
    id: typing.Optional[str] = Field(
        min_length=1, 
        description=(
            "Element ID. It must be unique within the root element. It "
            "is used as`accessibilityIdentifier` on iOS."
        ),
    )
    image_url: str = Field(
        format="uri", 
        description="Direct URL to an image.",
    )
    longtap_actions: typing.Optional[typing.List[div_action.DivAction]] = Field(
        min_items=1, 
        description=(
            "Action when long-clicking on an element. Doesn\'t work on "
            "the devices w/o touchgestures."
        ),
    )
    margins: typing.Optional[div_edge_insets.DivEdgeInsets] = Field(
        description="External margins from the element stroke.",
    )
    paddings: typing.Optional[div_edge_insets.DivEdgeInsets] = Field(
        description="Internal margins from the element stroke.",
    )
    placeholder_color: typing.Optional[str] = Field(
        format="color", 
        description="Placeholder background before the image is loaded.",
    )
    preload_required: typing.Optional[bool] = Field(
        description="Background image must be loaded before the display.",
    )
    preview: typing.Optional[str] = Field(
        min_length=1, 
        description=(
            "Image preview encoded in `base64`. It will be shown instead "
            "of`placeholder_color` before the image is loaded. Format "
            "`data url`:`data:[;base64],<data>`"
        ),
    )
    row_span: typing.Optional[int] = Field(
        description=(
            "Merges cells in a string of the [grid](div-grid.md) "
            "element."
        ),
    )
    scale: typing.Optional[div_image_scale.DivImageScale] = Field(
        description=(
            "Image scaling:`fit` places the entire image into the "
            "element (free space isfilled with background);`fill` scales "
            "the image to the element size and cuts offthe excess."
        ),
    )
    selected_actions: typing.Optional[typing.List[div_action.DivAction]] = Field(
        min_items=1, 
        description=(
            "List of [actions](div-action.md) to be executed when "
            "selecting an element in[pager](div-pager.md)."
        ),
    )
    tint_color: typing.Optional[str] = Field(
        format="color", 
        description="New color of a contour image.",
    )
    tint_mode: typing.Optional[div_blend_mode.DivBlendMode] = Field(
        description="The blend mode of color specified in tint_color.",
    )
    tooltips: typing.Optional[typing.List[div_tooltip.DivTooltip]] = Field(
        min_items=1, 
        description=(
            "Tooltips linked to an element. A tooltip can be shown "
            "by`div-action://show_tooltip?id=`, hidden by "
            "`div-action://hide_tooltip?id=` where`id` — tooltip id."
        ),
    )
    transform: typing.Optional[div_transform.DivTransform] = Field(
        description=(
            "Transformation of the element. Applies the passed transform "
            "to the element. Thecontent that does not fit into the "
            "original view will be cut off."
        ),
    )
    transition_change: typing.Optional[div_change_transition.DivChangeTransition] = Field(
        description=(
            "Change animation. It is played when the position or size of "
            "an element changes inthe new layout."
        ),
    )
    transition_in: typing.Optional[div_appearance_transition.DivAppearanceTransition] = Field(
        description=(
            "Appearance animation. It is played when an element with a "
            "new ID appears. Tolearn more about the concept of "
            "transitions, see "
            "[Animatedtransitions](../../interaction.dita#animation/tran"
            "sition-animation)."
        ),
    )
    transition_out: typing.Optional[div_appearance_transition.DivAppearanceTransition] = Field(
        description=(
            "Disappearance animation. It is played when an element "
            "disappears in the newlayout."
        ),
    )
    transition_triggers: typing.Optional[typing.List[div_transition_trigger.DivTransitionTrigger]] = Field(
        min_items=1, 
        description=(
            "Animation starting triggers. Default value: `[state_change, "
            "visibility_change]`."
        ),
    )
    visibility: typing.Optional[div_visibility.DivVisibility] = Field(
        description="Element visibility.",
    )
    visibility_action: typing.Optional[div_visibility_action.DivVisibilityAction] = Field(
        description=(
            "Tracking visibility of a single element. Not used if the "
            "`visibility_actions`parameter is set."
        ),
    )
    visibility_actions: typing.Optional[typing.List[div_visibility_action.DivVisibilityAction]] = Field(
        min_items=1, 
        description="Actions when an element appears on the screen.",
    )
    width: typing.Optional[div_size.DivSize] = Field(
        description="Element width.",
    )


DivImage.update_forward_refs()
