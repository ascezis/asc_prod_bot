import React, { useState, useEffect } from "react";
import { Box, Flex, useColorMode } from "@chakra-ui/react";
import { motion } from "framer-motion";
import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import Clients from "./pages/Clients";
import Projects from "./pages/Projects";
import Users from "./pages/Users";
import Login from "./pages/Login";
import Register from "./pages/Register";
import { getToken, getUser } from "./api/auth";

const MotionBox = motion(Box);

function App() {
  const [activeTab, setActiveTab] = useState("dashboard");
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [showRegister, setShowRegister] = useState(false);
  const { colorMode } = useColorMode();

  useEffect(() => {
    // Проверяем наличие токена при загрузке
    const token = getToken();
    const user = getUser();
    
    // Проверяем, нужно ли показать регистрацию
    const path = window.location.pathname;
    if (path === "/register" || path.includes("register")) {
      setShowRegister(true);
    }
    
    if (token && user) {
      setIsAuthenticated(true);
    } else {
      setIsAuthenticated(false);
    }
    setLoading(false);
  }, []);

  const colors = {
    light: {
      bg: "#f7fafc",
      sidebarBg: "#2b6cb0",
    },
    dark: {
      bg: "#1a202c",
      sidebarBg: "#2c5282",
    },
  };

  const currentColors = colorMode === "light" ? colors.light : colors.dark;

  // Показываем загрузку
  if (loading) {
    return null; // Можно добавить спиннер
  }

  // Если не авторизован, показываем страницу входа или регистрации
  if (!isAuthenticated) {
    if (showRegister) {
      return (
        <Register
          onRegister={() => {
            setShowRegister(false);
            setIsAuthenticated(false);
            window.location.href = "/";
          }}
        />
      );
    }
    return (
      <Login
        onLogin={() => setIsAuthenticated(true)}
        onShowRegister={() => setShowRegister(true)}
      />
    );
  }

  const renderContent = () => {
    switch (activeTab) {
      case "dashboard":
        return <Dashboard />;
      case "clients":
        return <Clients />;
      case "projects":
        return <Projects />;
      case "users":
        return <Users />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <MotionBox
      minH="100vh"
      bg={currentColors.bg}
      animate={{ backgroundColor: currentColors.bg }}
      transition={{ duration: 0.5 }}
      display="flex"
    >
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      <Box flex="1" p={8}>
        {renderContent()}
      </Box>
    </MotionBox>
  );
}

export default App;
