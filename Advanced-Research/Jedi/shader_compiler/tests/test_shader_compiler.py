from __future__ import annotations

from shader_compiler.pipeline import ASTParser, CodeGenerator, Optimizer, ShaderPipeline

SOURCE = """uniform vec4 color;
float brightness = 1.0;
float final = brightness * 2.0;
return vec4(color.rgb * final, 1.0);"""


def test_parser() -> None:
    ast = ASTParser().parse(SOURCE)
    assert "color" in ast.uniforms
    assert len(ast.nodes) > 0


def test_optimizer() -> None:
    ast = ASTParser().parse(SOURCE)
    optimized = Optimizer().optimize(ast)
    assert len(optimized.nodes) > 0


def test_code_generator() -> None:
    ast = ASTParser().parse(SOURCE)
    shader = CodeGenerator().generate(ast)
    assert "uniform" in shader.source
    assert "main" in shader.source


def test_full_pipeline() -> None:
    pipeline = ShaderPipeline()
    shader = pipeline.compile(SOURCE)
    assert shader.uniform_count == 1
    assert shader.instruction_count > 0


def test_empty_source() -> None:
    pipeline = ShaderPipeline()
    shader = pipeline.compile("")
    assert shader.uniform_count == 0

