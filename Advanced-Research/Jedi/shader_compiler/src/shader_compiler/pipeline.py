from __future__ import annotations

from .models import CompiledShader, ShaderAST


class ASTParser:
    def parse(self, source: str) -> ShaderAST:
        nodes: list[dict[str, str]] = []
        uniforms: list[str] = []
        for line in source.split("\n"):
            line = line.strip()
            if line.startswith("uniform"):
                parts = line.split()
                if len(parts) >= 3:
                    uniforms.append(parts[-1].rstrip(";"))
            elif "=" in line:
                parts = line.split("=", 1)
                nodes.append(
                    {
                        "type": "assignment",
                        "target": parts[0].strip(),
                        "value": parts[1].strip(),
                    }
                )
            elif line.startswith("return"):
                val = line.replace("return", "").strip().rstrip(";")
                nodes.append({"type": "return", "value": val})
        return ShaderAST(source=source, nodes=nodes, uniforms=uniforms)


class Optimizer:
    def optimize(self, ast: ShaderAST) -> ShaderAST:
        optimized_nodes: list[dict[str, str]] = []
        seen_targets: set[str] = set()
        for node in ast.nodes:
            if node["type"] == "assignment":
                if node["target"] in seen_targets:
                    optimized_nodes.append(
                        {"type": "assignment", "target": node["target"], "value": node["value"]}
                    )
                else:
                    seen_targets.add(node["target"])
                    optimized_nodes.append(node)
            else:
                optimized_nodes.append(node)
        ast.nodes = optimized_nodes
        return ast


class CodeGenerator:
    def generate(self, ast: ShaderAST) -> CompiledShader:
        lines: list[str] = []
        lines.append("// Generated shader")
        for u in ast.uniforms:
            lines.append(f"uniform vec4 {u};")
        lines.append("void main() {")
        for node in ast.nodes:
            if node["type"] == "assignment":
                lines.append(f"  float {node['target']} = {node['value']};")
            elif node["type"] == "return":
                lines.append(f"  gl_FragColor = {node['value']};")
        lines.append("}")
        source = "\n".join(lines)
        return CompiledShader(
            shader_id="compiled",
            source=source,
            uniform_count=len(ast.uniforms),
            instruction_count=len(ast.nodes),
        )


class ShaderPipeline:
    def __init__(self) -> None:
        self.parser = ASTParser()
        self.optimizer = Optimizer()
        self.generator = CodeGenerator()

    def compile(self, source: str) -> CompiledShader:
        ast = self.parser.parse(source)
        ast = self.optimizer.optimize(ast)
        return self.generator.generate(ast)
