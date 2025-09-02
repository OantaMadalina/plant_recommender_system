import React, { FC } from 'react';
import { BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import './App.css';
import Header from './components/Header/Header';
import Home from './components/Home/Home';
import MyRecipes from './components/MyRecipes/MyRecipes';
import Recipe from './components/Recipe/Recipe';
import CreateRecipe from './components/CreateRecipe/CreateRecipe';
import Footer from './components/Footer/Footer';

const App: FC = () => {
  return (
    <Router>
      <Header />
      <main>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/recipes" element={<MyRecipes />} />
        <Route path="/recipes/:recipeId" element={<Recipe />} />
        <Route path="/recipes/create" element={<CreateRecipe />} />
        <Route path="*" element={<Home />} />
      </Routes>
      </main>
      <Footer />
    </Router>
  );
};

export default App;