import React from 'react';
import { Button } from '../ui/button';

interface SearchBarProps {
  onSearch?: (query: string) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch }) => {
  const [searchQuery, setSearchQuery] = React.useState('');

  const handleSearch = () => {
    onSearch?.(searchQuery);
  };

  return (
    <div className="bg-white dark:bg-stone-800 shadow rounded-lg p-4 flex items-center justify-between min-h-[60px] space-x-4">
      <div className="w-full h-12 p-3 border border-dashed border-stone-300 dark:border-stone-600 rounded bg-stone-50 dark:bg-stone-700 text-sm text-stone-500 dark:text-stone-400 flex items-center justify-center">
        <input 
          type="text" 
          placeholder="Search" 
          className="w-full text-white bg-transparent focus:outline-none focus:ring-0" 
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
        />
      </div>
      <Button variant="outline" className="h-12" onClick={handleSearch}>
        Search
      </Button>
    </div>
  );
};

export default SearchBar; 