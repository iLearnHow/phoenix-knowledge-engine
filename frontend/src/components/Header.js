import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import styled from 'styled-components';
import { BookOpen, Plus, List, Home } from 'lucide-react';

const HeaderContainer = styled.header`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: white;
  border-bottom: 1px solid #e5e7eb;
  z-index: 1000;
  padding: 0 1rem;
`;

const HeaderContent = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 4rem;
`;

const Logo = styled(Link)`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  text-decoration: none;
  
  &:hover {
    color: #3b82f6;
  }
`;

const Nav = styled.nav`
  display: flex;
  align-items: center;
  gap: 1rem;
`;

const NavLink = styled(Link)`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  color: #6b7280;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s;
  
  &:hover {
    color: #3b82f6;
    background-color: #f1f5f9;
  }
  
  &.active {
    color: #3b82f6;
    background-color: #eff6ff;
  }
`;

function Header() {
  const location = useLocation();
  
  return (
    <HeaderContainer>
      <HeaderContent>
        <Logo to="/">
          <BookOpen size={24} />
          Phoenix Knowledge Engine
        </Logo>
        
        <Nav>
          <NavLink to="/" className={location.pathname === '/' ? 'active' : ''}>
            <Home size={20} />
            Home
          </NavLink>
          <NavLink to="/generate" className={location.pathname === '/generate' ? 'active' : ''}>
            <Plus size={20} />
            Generate
          </NavLink>
          <NavLink to="/learning-objectives" className={location.pathname === '/learning-objectives' ? 'active' : ''}>
            <List size={20} />
            Content
          </NavLink>
        </Nav>
      </HeaderContent>
    </HeaderContainer>
  );
}

export default Header;
