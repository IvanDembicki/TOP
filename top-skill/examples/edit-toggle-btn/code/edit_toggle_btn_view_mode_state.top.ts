import { DomContent, DomNode } from "../runtime";
import { TreeEditorNode } from "../tree_editor.top";

export class EditToggleBtnViewModeStateNode extends DomNode implements EditToggleBtnViewModeStateControllerAccess {
  private readonly _editor: TreeEditorNode;

  constructor(parent: DomNode) {
    super(parent);
    const editor = this.findUpByType(TreeEditorNode);
    if (!editor) throw new Error("EditToggleBtnViewModeState requires TreeEditor ancestor");
    this._editor = editor;
    this.setContent(new EditToggleBtnViewModeStateContent(this));
  }

  requestToggleMode(): void {
    this._editor.toggleEditMode();
  }

  getActionLabelText(): string {
    return "Edit mode";
  }

  getActionClassToken(): string {
    return "edit-toggle-btn-state";
  }
}

interface EditToggleBtnViewModeStateContentAccess {
  getView(): HTMLElement;
}

interface EditToggleBtnViewModeStateControllerAccess {
  getActionLabelText(): string;
  getActionClassToken(): string;
  requestToggleMode(): void;
}

class EditToggleBtnViewModeStateContent extends DomContent implements EditToggleBtnViewModeStateContentAccess {
  constructor(private readonly controller: EditToggleBtnViewModeStateControllerAccess) {
    const el = document.createElement("button");
    el.className = controller.getActionClassToken();
    el.textContent = controller.getActionLabelText();
    super(el);
    el.addEventListener("click", (event) => this.onClick(event));
  }

  private onClick(event: MouseEvent): void {
    event.stopPropagation();
    this.controller.requestToggleMode();
  }
}
