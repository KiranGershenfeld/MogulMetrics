import AppContainer from './components/AppContainer';
import LifecycleContainer from './components/Lifecycle';
import AboutPage from './components/AboutPage';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  Navigate,
} from 'react-router-dom';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <title>Mogul Metrics</title>
          <div className="page-content">
            <Routes> 
              <Route exact path='/' exact element={ <Navigate to={'/main?channel_id=UCrPseYLGpNygVi34QpGNqpA'} />} />
              <Route exact path='/main' exact element={ <AppContainer />} />
              <Route exact path='videolifecycle' exact element={<LifecycleContainer/>} />
              <Route exact path='about' exact element={<AboutPage/>} />
            </Routes>
          </div>
        </header>
      </div>
    </Router>
  );
}

export default App;
