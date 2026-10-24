import { useState, useEffect } from "react";

const STORAGE_KEY = "equation-favorites";

export function useFavorites() {
  const [favorites, setFavorites] = useState<Set<number>>(new Set());
  const [isLoaded, setIsLoaded] = useState(false);

  // Load from localStorage on mount
  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      try {
        const ids = JSON.parse(stored) as number[];
        setFavorites(new Set(ids));
      } catch {
        setFavorites(new Set());
      }
    }
    setIsLoaded(true);
  }, []);

  // Save to localStorage whenever favorites change
  useEffect(() => {
    if (isLoaded) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(Array.from(favorites)));
    }
  }, [favorites, isLoaded]);

  const toggleFavorite = (id: number) => {
    setFavorites(prev => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  return { favorites, toggleFavorite };
}
