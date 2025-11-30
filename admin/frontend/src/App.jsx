import React, { useState } from "react";
import { Box, Flex, useColorMode } from "@chakra-ui/react";
import { motion } from "framer-motion";
import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import Clients from "./pages/Clients";
import Projects from "./pages/Projects";

const MotionBox = motion(Box);

function App() {
  const [activeTab, setActiveTab] = useState("dashboard");
  const { colorMode } = useColorMode();

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

  const renderContent = () => {
    switch (activeTab) {
      case "dashboard":
        return <Dashboard />;
      case "clients":
        return <Clients />;
      case "projects":
        return <Projects />;
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
