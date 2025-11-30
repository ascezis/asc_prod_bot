import React from "react";
import {
  Box,
  VStack,
  Button,
  Heading,
  IconButton,
  Flex,
  useColorMode,
  Text,
} from "@chakra-ui/react";
import { SunIcon, MoonIcon } from "@chakra-ui/icons";
import { motion, AnimatePresence } from "framer-motion";
import { getUser, logout } from "../api/auth";

const MotionBox = motion(Box);

function Sidebar({ activeTab, setActiveTab }) {
  const { colorMode, toggleColorMode } = useColorMode();
  const user = getUser();

  const handleLogout = () => {
    logout();
    window.location.reload();
  };

  const colors = {
    light: {
      sidebarBg: "#2b6cb0",
    },
    dark: {
      sidebarBg: "#2c5282",
    },
  };

  const currentColors = colorMode === "light" ? colors.light : colors.dark;

  const menuItems = [
    { id: "dashboard", label: "📊 Dashboard" },
    { id: "clients", label: "👥 Clients" },
    { id: "projects", label: "📁 Projects" },
  ];

  return (
    <MotionBox
      w="250px"
      bg={currentColors.sidebarBg}
      color="white"
      p={6}
      shadow="lg"
      display="flex"
      flexDirection="column"
      minH="100vh"
      animate={{ backgroundColor: currentColors.sidebarBg }}
      transition={{ duration: 0.5 }}
    >
      <Flex justify="space-between" align="center" mb={8}>
        <Heading size="md">Admin Panel</Heading>
        <IconButton
          aria-label="Toggle theme"
          onClick={toggleColorMode}
          size="sm"
          variant="ghost"
          color="white"
        >
          <Box
            w="24px"
            h="24px"
            position="relative"
            display="flex"
            justifyContent="center"
            alignItems="center"
          >
            <AnimatePresence exitBeforeEnter initial={false}>
              {colorMode === "light" ? (
                <motion.div
                  key="moon"
                  initial={{ rotate: -90, scale: 0, opacity: 0 }}
                  animate={{ rotate: 0, scale: 1, opacity: 1 }}
                  exit={{ rotate: 90, scale: 0, opacity: 0 }}
                  transition={{ duration: 0.5 }}
                  style={{ position: "absolute" }}
                >
                  <MoonIcon />
                </motion.div>
              ) : (
                <motion.div
                  key="sun"
                  initial={{ rotate: 90, scale: 0, opacity: 0 }}
                  animate={{ rotate: 0, scale: 1, opacity: 1 }}
                  exit={{ rotate: -90, scale: 0, opacity: 0 }}
                  transition={{ duration: 0.5 }}
                  style={{ position: "absolute" }}
                >
                  <SunIcon />
                </motion.div>
              )}
            </AnimatePresence>
          </Box>
        </IconButton>
      </Flex>
      <VStack align="start" spacing={4} flex="1">
        {menuItems.map((item) => (
          <Button
            key={item.id}
            variant={activeTab === item.id ? "solid" : "ghost"}
            colorScheme="whiteAlpha"
            w="100%"
            justifyContent="flex-start"
            _hover={{ bg: "blue.600" }}
            onClick={() => setActiveTab(item.id)}
          >
            {item.label}
          </Button>
        ))}
      </VStack>
      
      <Box mt="auto" pt={4} borderTop="1px solid" borderColor="whiteAlpha.300">
        {user && (
          <Text fontSize="sm" mb={2} opacity={0.9}>
            {user.username} ({user.role})
          </Text>
        )}
        <Button
          variant="ghost"
          colorScheme="whiteAlpha"
          w="100%"
          size="sm"
          onClick={handleLogout}
        >
          Выйти
        </Button>
      </Box>
    </MotionBox>
  );
}

export default Sidebar;
