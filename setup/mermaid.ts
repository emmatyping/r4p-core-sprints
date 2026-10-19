import { defineMermaidSetup } from '@slidev/types'

export default defineMermaidSetup(() => ({
  theme: 'base',
  themeCSS: '.edgeLabel span.edgeLabel { display: inline-block; border: 1px solid #c78350; border-radius: 6px; padding: 3px 7px; }',
  themeVariables: {
    primaryColor: '#f6cfa9',
    primaryBorderColor: '#f97316',
    primaryTextColor: '#6b5b50',
    textColor: '#6b5b50',
    lineColor: '#c2410c',
    secondaryColor: '#fff7ed',
    tertiaryColor: '#fff7ed',
    edgeLabelBackground: '#ffedd5',
    fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif',
  },
  sequence: { mirrorActors: false, actorMargin: 40, messageMargin: 28 },
  flowchart: { padding: 10, nodeSpacing: 35, rankSpacing: 45, curve: 'basis' },
}))
