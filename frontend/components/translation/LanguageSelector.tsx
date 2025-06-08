import React from 'react';
import { PlusIcon } from 'lucide-react';

interface LanguageSelectorProps {
  onAddLanguage?: () => void;
}

const LanguageSelector: React.FC<LanguageSelectorProps> = ({ onAddLanguage }) => {
  return (
    <div>
      <h2 className="text-lg font-semibold mb-3 text-stone-700 dark:text-stone-300">
        Languages
      </h2>
      <div className="p-3 border border-dashed border-stone-300 dark:border-stone-600 rounded bg-stone-50 dark:bg-stone-700 text-sm text-stone-500 dark:text-stone-400 min-h-[50px] flex items-center justify-center">
        <PlusIcon 
          className="w-4 h-4 cursor-pointer hover:text-stone-700 dark:hover:text-stone-200" 
          onClick={onAddLanguage}
        />
      </div>
    </div>
  );
};

export default LanguageSelector; 