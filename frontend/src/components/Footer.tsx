import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-slate-100 text-slate-700 py-6 px-4 border-t border-slate-200">
      <div className="container mx-auto">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <p className="text-sm">Secure Chat Interface - All communications are encrypted</p>
          </div>
          <div className="text-center md:text-right">
            <p className="font-semibold">Developed by: HUDA NOOR</p>
            <p className="text-sm">Description: Advanced chat API & frontend integration with AI agent and MCP tools</p>
          </div>
        </div>
        <div className="mt-4 pt-4 border-t border-slate-300 text-center text-xs text-slate-500">
          <p>© {new Date().getFullYear()} Chat API & Frontend Integration. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;