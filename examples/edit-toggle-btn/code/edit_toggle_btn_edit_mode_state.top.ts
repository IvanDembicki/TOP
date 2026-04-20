import { DomContent, DomNode } from "../runtime";
import { TreeEditorNode } from "../tree_editor.top";

export class EditToggleBtnEditModeStateNode extends DomNode implements EditToggleBtnEditModeStateControllerAccess {
  private readonly _editor: TreeEditorNode;

  constructor(parent: DomNode) {
    super(parent);
    const editor = this.findUpByType(TreeEditorNode);
    if (!editor) throw new Error("EditToggleBtnEditModeState requires TreeEditor ancestor");
    this._editor = editor;
    this.setContent(new EditToggleBtnEditModeStateContent(this));
  }

  requestToggleMode(): void {
    this._editor.toggleEditMode();
  }
}

interface EditToggleBtnEditModeStateContentAccess {
  getView(): HTMLElement;
}

interface EditToggleBtnEditModeStateControllerAccess {
  requestToggleMode(): void;
}

class EditToggleBtnEditModeStateContent extends DomContent implements EditToggleBtnEditModeStateContentAccess {
  constructor(private readonly controller: EditToggleBtnEditModeStateControllerAccess) {
    const el = document.createElement("button");
    el.className = "edit-toggle-btn-state active";
    el.textContent = "View mode";
    super(el);
    el.addEventListener("click", (event) => this.onClick(event));
  }

  private onClick(event: MouseEvent): void {
    event.stopPropagation();
    this.controller.requestToggleMode();
  }
}
