import './styles/index.css';

import React from 'react';
import ReactDOM from 'react-dom';
import Main from './components/main';

// Render App
ReactDOM.render(
  <div className="flex flex-col min-h-screen">
    <Main />
  </div>,
  document.getElementById('root'),
);

if (import.meta.hot) {
  import.meta.hot.accept();
}
