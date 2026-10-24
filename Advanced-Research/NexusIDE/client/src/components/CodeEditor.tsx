import { FC, useRef, useEffect } from "react";
import * as monaco from "monaco-editor";
import { editor } from "monaco-editor";

interface CodeEditorProps {
  code: string;
  language: string;
  onChange: (value: string) => void;
}

// Define languages for syntax highlighting
const languageMap: Record<string, string> = {
  js: "javascript",
  jsx: "javascript",
  ts: "typescript",
  tsx: "typescript",
  py: "python",
  rb: "ruby",
  java: "java",
  json: "json",
  html: "html",
  css: "css",
  md: "markdown",
  go: "go",
  rs: "rust",
  c: "c",
  cpp: "cpp",
  cs: "csharp",
  php: "php",
  sh: "shell",
  yaml: "yaml",
  sql: "sql",
  txt: "plaintext"
};

const getLanguageFromFileName = (fileName: string): string => {
  const extension = fileName.split('.').pop() || "";
  return languageMap[extension] || "plaintext";
};

const CodeEditor: FC<CodeEditorProps> = ({ code, language, onChange }) => {
  const editorRef = useRef<HTMLDivElement>(null);
  const monacoEditorRef = useRef<editor.IStandaloneCodeEditor | null>(null);

  useEffect(() => {
    if (editorRef.current) {
      // Initialize Monaco editor
      monacoEditorRef.current = monaco.editor.create(editorRef.current, {
        value: code,
        language: getLanguageFromFileName(language),
        theme: 'vs-dark',
        automaticLayout: true,
        minimap: { enabled: false },
        scrollBeyondLastLine: false,
        lineNumbers: 'on',
        renderLineHighlight: 'all',
        fontSize: 13,
        fontFamily: '"JetBrains Mono", "Droid Sans Mono", monospace',
        tabSize: 2,
        rulers: [],
        wordWrap: 'on',
        autoClosingBrackets: 'always',
        autoClosingQuotes: 'always',
        formatOnType: true,
      });

      // Expose monaco to window for Range constructor
      (window as any).monaco = monaco;

      // Add event listener for content changes
      monacoEditorRef.current.onDidChangeModelContent(() => {
        const value = monacoEditorRef.current?.getValue() || "";
        onChange(value);
      });

      // Clean up
      return () => {
        monacoEditorRef.current?.dispose();
      };
    }
  }, []);

  // Update editor value if code prop changes
  useEffect(() => {
    if (monacoEditorRef.current) {
      const currentValue = monacoEditorRef.current.getValue();
      if (code !== currentValue) {
        // Preserving cursor position while updating
        const position = monacoEditorRef.current.getPosition();
        monacoEditorRef.current.setValue(code);
        if (position) {
          monacoEditorRef.current.setPosition(position);
        }
      }
    }
  }, [code]);

  // Expose monaco instance to window for global access (hacky but useful for AccessoryBar)
  useEffect(() => {
    if (monacoEditorRef.current) {
      (window as any).monacoEditor = monacoEditorRef.current;
    }
    return () => {
      (window as any).monacoEditor = null;
    };
  }, [monacoEditorRef.current]);

  // Update editor language if language prop changes
  useEffect(() => {
    if (monacoEditorRef.current) {
      const model = monacoEditorRef.current.getModel();
      if (model) {
        monaco.editor.setModelLanguage(model, getLanguageFromFileName(language));
      }
    }
  }, [language]);

  return (
    <div className="flex-1 overflow-hidden">
      <div ref={editorRef} className="h-full w-full"></div>
    </div>
  );
};

export default CodeEditor;
