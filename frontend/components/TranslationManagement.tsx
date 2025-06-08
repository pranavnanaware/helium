import React from 'react';
import ProjectSelector from './translation/ProjectSelector';
import LanguageSelector from './translation/LanguageSelector';
import SearchBar from './translation/SearchBar';
import TranslationEditor from './translation/TranslationEditor';

const TranslationManagement = () => {
  const handleAddProject = () => {
    console.log("Add project clicked");
  };

  const handleAddLanguage = () => {
    console.log("Add language clicked");
  };

  const handleSearch = (query: string) => {
    console.log("Search query:", query);
  };

  return (
    <div className="flex flex-grow container mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Sidebar */}
      <aside className="w-1/4 xl:w-1/5 p-4 bg-white dark:bg-stone-800 shadow rounded-lg mr-8 space-y-6">
        <ProjectSelector onAddProject={handleAddProject} />
        <LanguageSelector onAddLanguage={handleAddLanguage} />
      </aside>

      {/* Main Content Area */}
      <main className="w-3/4 xl:w-4/5 flex flex-col space-y-6">
        <SearchBar onSearch={handleSearch} />
        <TranslationEditor />
      </main>
    </div>
  );
};

export default TranslationManagement;