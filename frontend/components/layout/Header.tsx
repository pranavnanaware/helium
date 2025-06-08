import React from 'react';

const Header = () => {
  return (
    <header className="bg-white dark:bg-stone-800 shadow-md sticky top-0 z-50">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <span className="text-xl font-semibold text-stone-700 dark:text-stone-200">
              Helium
            </span>
          </div>
          <nav className="flex items-center space-x-4">
            <div className="text-sm p-2 border border-dashed border-stone-300 dark:border-stone-600 rounded-md text-stone-500 dark:text-stone-400">
              [User Profile Placeholder]
            </div>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header; 