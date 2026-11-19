# UI references before frontend code

A short step at the start of any task that changes user interface. It is part
of the same task and pull request, not a separate one.

## Steps

1. **Owner mockup first.** If the task, its change folder or the pull request
   has a mockup (Figma link or image), follow it. References only fill gaps.
2. **Look.** Find 3–5 references for the screen or component: a pattern
   library such as Mobbin (through its connector if your agent has one), and
   strong products that solve the same job. One intent per search ("settings
   page", "review queue with approve and reject"). Look at the images; do not
   judge from titles.
3. **Assess.** For each reference: what it solves well, what fits your users,
   what does not fit your principles.
4. **Code** with the project's design system. Take patterns, never logos,
   icons, illustrations or copy.
5. **Note it** in the pull request under "UI references": links and one line
   each on what was taken. Do not commit reference images.

## Principles for a clean interface

- One screen, one main job; the answer first, details one click away.
- Plain words from the glossary.
- Every state exists: loading, empty, error, partial, no permission.
- Keyboard works everywhere; visible focus; WCAG AA contrast.
- Calm look: neutral palette, one accent colour, consistent spacing.
