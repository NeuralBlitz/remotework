import { useState, useMemo } from "react";
import { useEquations } from "@/hooks/use-equations";
import { CyberCard } from "@/components/CyberCard";
import { LatexDisplay } from "@/components/LatexDisplay";
import { CyberButton } from "@/components/CyberButton";
import { Link } from "wouter";
import { Search, Loader2, Heart } from "lucide-react";
import { motion } from "framer-motion";
import { useFavorites } from "@/hooks/use-favorites";

const CATEGORIES = [
  "All",
  "Tensor Dynamics",
  "Number Theory",
  "Neural Architecture",
  "Ethics",
  "Quantum Gravity",
  "Set Theory",
  "Quantum Computation",
  "Arithmetic Geometry",
  "Topology",
  "Hodge Theory",
  "Ontology",
  "Metaphysics",
  "Quantum Field Theory",
  "Cryptography",
  "Optimization",
  "Information Theory",
  "Semantics",
  "Verification",
  "Epistemology",
  "Computation"
];

export default function EquationIndex() {
  const [search, setSearch] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [showFavoritesOnly, setShowFavoritesOnly] = useState(false);
  const { data: equations, isLoading, error } = useEquations(search);
  const { favorites, toggleFavorite } = useFavorites();

  const filtered = useMemo(() => {
    if (!equations) return [];
    let result = equations;
    
    if (selectedCategory !== "All") {
      result = result.filter(eq => eq.category === selectedCategory);
    }
    
    if (showFavoritesOnly) {
      result = result.filter(eq => favorites.has(eq.id));
    }
    
    return result;
  }, [equations, selectedCategory, showFavoritesOnly, favorites]);

  return (
    <div className="space-y-6 md:space-y-8">
      <div className="flex flex-col gap-6">
        <div>
          <h1 className="text-3xl sm:text-4xl md:text-4xl font-display font-bold text-white mb-2">
            HYPER<span className="text-secondary">-AXIOMATIC</span> INDEX
          </h1>
          <p className="font-mono text-primary/60 text-xs sm:text-sm">
            // ACCESSING ARCHIVES... // FOUND {filtered?.length || 0} ENTRIES
          </p>
        </div>
        
        <div className="relative w-full group">
          <div className="absolute inset-y-0 left-3 flex items-center pointer-events-none text-primary/50 group-focus-within:text-primary">
            <Search className="w-4 sm:w-5 h-4 sm:h-5" />
          </div>
          <input
            type="text"
            placeholder="SEARCH_BY_CODE_OR_TITLE"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full bg-black/40 border border-primary/30 text-primary px-10 py-2 sm:py-3 font-mono text-xs sm:text-sm focus:outline-none focus:border-primary focus:shadow-[0_0_15px_rgba(0,240,255,0.3)] transition-all placeholder:text-primary/20"
            data-testid="input-search"
          />
          <div className="absolute inset-0 border border-transparent group-focus-within:border-primary/50 pointer-events-none animate-pulse" />
        </div>
      </div>

      {/* Category Filter */}
      <div className="space-y-2">
        <p className="text-xs font-mono text-primary/60 uppercase tracking-wider">Filter by Category</p>
        <div className="flex flex-wrap gap-2">
          {CATEGORIES.map(cat => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              data-testid={`button-category-${cat}`}
              className={`px-3 py-1 text-xs font-mono uppercase transition-all ${
                selectedCategory === cat
                  ? 'bg-primary text-black border border-primary'
                  : 'bg-black/40 text-primary border border-primary/30 hover:border-primary'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Favorites Toggle */}
      <div className="flex items-center gap-3">
        <button
          onClick={() => setShowFavoritesOnly(!showFavoritesOnly)}
          data-testid="button-toggle-favorites"
          className={`flex items-center gap-2 px-4 py-2 border transition-all text-sm font-mono ${
            showFavoritesOnly
              ? 'bg-secondary text-black border-secondary shadow-[0_0_15px_rgba(188,19,254,0.4)]'
              : 'bg-black/40 text-secondary border-secondary/30 hover:border-secondary'
          }`}
        >
          <Heart className="w-4 h-4" />
          FAVORITES ONLY
        </button>
        <span className="text-xs text-primary/60 font-mono">({favorites.size} saved)</span>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center py-32">
          <Loader2 className="w-12 h-12 text-primary animate-spin" />
        </div>
      ) : error ? (
        <div className="p-6 sm:p-8 border border-destructive/50 bg-destructive/10 text-center text-destructive">
          <h3 className="font-bold text-base sm:text-lg mb-2">ERROR FETCHING DATA</h3>
          <p className="font-mono text-xs sm:text-sm">{error.message}</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
          {filtered?.map((eq, i) => (
            <Link key={eq.id} href={`/equations/${eq.id}`} className="block h-full" data-testid={`card-equation-${eq.id}`}>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
                className="h-full"
              >
                <CyberCard 
                  className="h-full hover:bg-white/5 cursor-pointer group relative"
                  title={eq.title}
                  code={eq.code}
                >
                  <div className="py-6 sm:py-8 flex items-center justify-center min-h-[100px] sm:min-h-[120px]">
                    <div className="text-base sm:text-lg text-white/90 group-hover:text-primary transition-colors duration-300 max-w-full overflow-hidden">
                      <LatexDisplay expression={eq.latex} />
                    </div>
                  </div>
                  
                  <div className="mt-4 pt-4 border-t border-white/10 flex justify-between items-center text-xs font-mono text-muted-foreground gap-2">
                    <span className="truncate">{eq.category}</span>
                    <button
                      onClick={(e) => {
                        e.preventDefault();
                        e.stopPropagation();
                        toggleFavorite(eq.id);
                      }}
                      data-testid={`button-favorite-${eq.id}`}
                      className="shrink-0 hover:text-secondary transition-colors"
                      title={favorites.has(eq.id) ? "Remove from favorites" : "Add to favorites"}
                    >
                      <Heart className={`w-4 h-4 ${favorites.has(eq.id) ? 'fill-secondary text-secondary' : ''}`} />
                    </button>
                  </div>
                </CyberCard>
              </motion.div>
            </Link>
          ))}
          
          {filtered?.length === 0 && (
            <div className="col-span-full py-16 sm:py-20 text-center border border-dashed border-white/10 rounded-lg">
              <p className="text-muted-foreground font-mono text-sm">NO DATA FOUND FOR QUERY</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
