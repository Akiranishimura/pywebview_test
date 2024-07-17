import "./Editor.css";

export function Editor() {

  return (
    <div className="editor-container">

      <button
        className="button"
        onClick={() => {
          window.pywebview.api.manual();
        }}
      >
        3V
      </button>
    </div>
  );
}
