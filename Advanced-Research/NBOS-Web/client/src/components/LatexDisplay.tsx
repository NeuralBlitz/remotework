import 'katex/dist/katex.min.css';
import { InlineMath, BlockMath } from 'react-katex';

interface LatexDisplayProps {
  expression: string;
  block?: boolean;
  className?: string;
  glow?: boolean;
}

export function LatexDisplay({ expression, block = false, className = "", glow = false }: LatexDisplayProps) {
  // Catch potential errors in latex rendering gracefully
  try {
    return (
      <div className={`${className} ${glow ? 'latex-glow' : ''} text-foreground overflow-x-auto`}>
        {block ? (
          <BlockMath math={expression} />
        ) : (
          <InlineMath math={expression} />
        )}
      </div>
    );
  } catch (e) {
    return <code className="text-destructive text-xs">Error rendering equation</code>;
  }
}
