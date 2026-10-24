# nebulawrap/client.py
import asyncio
from .providers.base import ProviderAdapter
from .provenance.golden_dag import build_decision_capsule

class NebulaClient:
    def __init__(self, provider: ProviderAdapter, safety_hooks=None, memory_manager=None):
        self.provider = provider
        self.safety_hooks = safety_hooks or []
        self.memory = memory_manager

    async def generate(self, prompt, **opts):
        # 1) optional: inject memory context
        if self.memory:
            ctx = await self.memory.retrieve(prompt)
            prompt = f"{ctx}\n\n{prompt}"

        # 2) pre-safety hooks
        for hook in self.safety_hooks:
            prompt = hook.pre_process(prompt)

        # 3) provider call
        result = await self.provider.generate(prompt, **opts)  # {'text':..., 'usage':...}

        # 4) post-safety hooks
        for hook in self.safety_hooks:
            result['text'] = hook.post_process(result['text'])

        # 5) provenance
        capsule = build_decision_capsule(prompt, self.provider.info(), result['text'], extra={'usage': result.get('usage')})
        result['decision_capsule'] = capsule
        return result

    async def stream(self, prompt, on_token, **opts):
        # streaming with same hooks
        if self.memory:
            ctx = await self.memory.retrieve(prompt)
            prompt = f"{ctx}\n\n{prompt}"
        for hook in self.safety_hooks:
            prompt = hook.pre_process(prompt)
        async for token in self.provider.stream(prompt, **opts):
            for hook in self.safety_hooks:
                token = hook.token_transform(token)
            on_token(token)
