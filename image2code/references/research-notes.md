# Prior Art And Lessons

This skill is not a replacement for a design-to-code product. It creates a structured image design pack and implementation workflow that Codex can use inside a repository.

## Relevant Tools

- `abi/screenshot-to-code`: converts screenshots, mockups, and Figma designs into HTML/Tailwind/React/Vue and other stacks with AI. Lesson: screenshot-to-code needs explicit stack targets and benefits from comparing multiple model outputs. Source: https://github.com/abi/screenshot-to-code
- `tldraw/make-real`: turns sketches and annotated canvases into working Tailwind/React prototypes. Lesson: rough visual inputs become more reliable when the agent preserves annotations, uses a constrained stack, and renders the result for inspection. Source: https://github.com/tldraw/make-real
- Uizard: generates designs from prompts or screenshots and can turn screenshots into editable mockups. Lesson: prompt/screenshot inputs are useful, but generated UI still needs a structured review and editable spec layer. Source: https://uizard.io/
- Builder.io Visual Copilot: converts Figma designs to framework-specific code and emphasizes component mapping and style preferences. Lesson: implementation quality improves when the handoff maps visual design to existing components/framework constraints. Source: https://www.builder.io/blog/figma-to-code-visual-copilot
- Figma Make: turns designs/prompts into functional prototypes and supports using design library context. Lesson: product style context and design-system rules should be first-class inputs, not afterthoughts. Source: https://www.figma.com/make/
- `dominikmartn/hue`: generates reusable brand design-language skills from URLs, screenshots, or descriptions, with structured design models, token/component documentation, and HTML previews. Lesson: Image2Code should borrow structured design provenance and preview discipline, but keep its output project-specific rather than becoming a brand-skill generator. Source: https://github.com/dominikmartn/hue

## Relevant Research

- Visual Prompting with Iterative Refinement for Design Critique Generation: iterative visual prompting can improve UI critique quality and visually ground feedback. Lesson: require critique rounds and record region-specific feedback. Source: https://arxiv.org/abs/2412.16829
- DCGen: screenshot-to-code generation often fails through omission, distortion, and misarrangement; segmenting large screenshots can improve results. Lesson: break complex pages into regions/components during implementation planning. Source: https://arxiv.org/abs/2406.16386
- VisRefiner: rendering, comparing visual differences, and refining code mirrors human screenshot-to-code work. Lesson: implementation mode should use browser screenshots and visual comparison loops, not one-pass coding. Source: https://arxiv.org/abs/2602.05998
- Design2Code: benchmarks multimodal models on converting screenshots to HTML/CSS and highlights the gap between plausible-looking code and pixel-faithful implementation. Lesson: store both target images and rendered implementation screenshots so fidelity can be reviewed explicitly. Source: https://arxiv.org/abs/2403.03163

## Practical Takeaways

- Separate visual generation from implementation specs.
- Preserve current product constraints for old-project redesigns.
- Generate multiple images: system, screens, states, responsive variants.
- Segment large screenshots into implementation regions before coding.
- Keep prompts and review logs for traceability.
- Keep a structured design model so token, component, icon, and screen decisions have provenance instead of living only in prose or pixels.
- Validate implementation by rendering the app, saving after-screenshots, and comparing them to the pack.
