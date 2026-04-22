import { DomContent, SwitchableNode, type TopNode } from "../runtime";
import { TreeEditorNode } from "../tree_editor.top";
import { EditToggleBtnEditModeStateNode } from "./edit_toggle_btn_edit_mode_state.top";
import { EditToggleBtnViewModeStateNode } from "./edit_toggle_btn_view_mode_state.top";

export class EditToggleBtnNode extends SwitchableNode {
  private readonly _editor: TreeEditorNode;
  private _viewMode!: EditToggleBtnViewModeStateNode;
  private _editMode!: EditToggleBtnEditModeStateNode;

  constructor(parent: TopNode) {
    super(parent);
    const editor = this.findUpByType(TreeEditorNode);
    if (!editor) throw new Error("EditToggleBtn requires TreeEditor ancestor");
    this._editor = editor;
    this.setContent(new EditToggleBtnContent(new EditToggleBtnControllerAccessZero()));
    this.buildChildren();
  }

  override refresh(): void {
    const target = this._editor.isEditMode ? this._editMode : this._viewMode;
    this.openChild(target);
  }

  private buildChildren(): void {
    this._viewMode = new EditToggleBtnViewModeStateNode(this);
    this._editMode = new EditToggleBtnEditModeStateNode(this);
    this.setInitialChild(this._viewMode);
  }
}

interface EditToggleBtnContentAccess {
  getView(): HTMLElement;
  mount(view: HTMLElement | null): void;
}

interface EditToggleBtnControllerAccess {}
class EditToggleBtnControllerAccessZero implements EditToggleBtnControllerAccess {}

class EditToggleBtnContent extends DomContent implements EditToggleBtnContentAccess {
  constructor(_controller: EditToggleBtnControllerAccess) {
    const el = document.createElement("div");
    el.className = "edit-toggle-btn";
    super(el);
  }
}
