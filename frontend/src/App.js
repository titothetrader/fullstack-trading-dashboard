import { Navbar } from './components';

import './App.css';


function App() {
  return (
    <div className="text-center">
      <header className="bg-blue-400">
        <Navbar />
      </header>
      <div>
        <h1 className="text-3xl underline text-white">Header</h1>
        <h1 className="text-2xl text-blue-400">Body</h1>
      </div>
    </div>
  );
}

export default App;
