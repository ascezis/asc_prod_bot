import React, { useEffect, useState } from "react";
import {
  Box,
  Heading,
  VStack,
  Button,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Flex,
  Spinner,
  Text,
  useDisclosure,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  ModalFooter,
  Input,
  FormControl,
  FormLabel,
  Badge,
  IconButton,
  useColorMode
} from "@chakra-ui/react";
import { SunIcon, MoonIcon } from "@chakra-ui/icons";
import axios from "axios";
import { motion, AnimatePresence } from "framer-motion";

const MotionBox = motion(Box);
const MotionText = motion(Text);
const MotionTr = motion(Tr);
const MotionTd = motion(Td);
const MotionBadge = motion(Badge);

function App() {
  const [clients, setClients] = useState([]);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState("clients");

  const { isOpen: isClientModalOpen, onOpen: onClientModalOpen, onClose: onClientModalClose } = useDisclosure();
  const { isOpen: isProjectModalOpen, onOpen: onProjectModalOpen, onClose: onProjectModalClose } = useDisclosure();

  const [newClient, setNewClient] = useState({ telegram_id: "", username: "", full_name: "" });
  const [newProject, setNewProject] = useState({ client_id: "", project_type: "", status: "" });

  const API_URL = "http://localhost:8000";

  const { colorMode, toggleColorMode } = useColorMode();

  // Цвета для плавной анимации
  const colors = {
    light: {
      bg: "#f7fafc",
      sidebarBg: "#2b6cb0",
      tableBg: "#fff",
      tableHover: "#ebf8ff",
      text: "#1a202c",
      tableHeaderClients: "#ebf8ff",
      tableHeaderProjects: "#b2f5ea"
    },
    dark: {
      bg: "#1a202c",
      sidebarBg: "#2c5282",
      tableBg: "#2d3748",
      tableHover: "#2a4365",
      text: "#edf2f7",
      tableHeaderClients: "#2c5282",
      tableHeaderProjects: "#285e61"
    }
  };

  const currentColors = colorMode === "light" ? colors.light : colors.dark;

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const clientsRes = await axios.get(`${API_URL}/clients`);
        const projectsRes = await axios.get(`${API_URL}/projects`);
        setClients(clientsRes.data);
        setProjects(projectsRes.data);
      } catch (err) {
        console.error("Ошибка загрузки данных:", err);
        setError("Не удалось загрузить данные с сервера");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleAddClient = async () => {
    try {
      const res = await axios.post(`${API_URL}/clients`, newClient);
      setClients([...clients, res.data]);
      setNewClient({ telegram_id: "", username: "", full_name: "" });
      onClientModalClose();
    } catch (err) {
      console.error(err);
      alert("Ошибка при добавлении клиента");
    }
  };

  const handleAddProject = async () => {
    try {
      const res = await axios.post(`${API_URL}/projects`, newProject);
      setProjects([...projects, res.data]);
      setNewProject({ client_id: "", project_type: "", status: "" });
      onProjectModalClose();
    } catch (err) {
      console.error(err);
      alert("Ошибка при добавлении проекта");
    }
  };

  if (loading) {
    return (
      <Flex justify="center" align="center" minH="100vh" bg={currentColors.bg}>
        <Spinner size="xl" />
      </Flex>
    );
  }

  if (error) {
    return (
      <Flex justify="center" align="center" minH="100vh" bg={currentColors.bg}>
        <Text color="red.500" fontSize="lg">{error}</Text>
      </Flex>
    );
  }

  return (
    <MotionBox
      minH="100vh"
      bg={currentColors.bg}
      color={currentColors.text}
      animate={{ backgroundColor: currentColors.bg, color: currentColors.text }}
      transition={{ duration: 0.5 }}
      display="flex"
    >
      {/* Sidebar */}
      <MotionBox
        w="250px"
        bg={currentColors.sidebarBg}
        color="white"
        p={6}
        shadow="lg"
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
        <VStack align="start" spacing={4}>
          <Button
            variant={activeTab === "clients" ? "solid" : "ghost"}
            colorScheme="whiteAlpha"
            w="100%"
            _hover={{ bg: "blue.600" }}
            onClick={() => setActiveTab("clients")}
          >
            Clients
          </Button>
          <Button
            variant={activeTab === "projects" ? "solid" : "ghost"}
            colorScheme="whiteAlpha"
            w="100%"
            _hover={{ bg: "blue.600" }}
            onClick={() => setActiveTab("projects")}
          >
            Projects
          </Button>
        </VStack>
      </MotionBox>

      {/* Main Content */}
      <MotionBox flex="1" p={10}>
        {activeTab === "clients" && (
          <>
            <Flex justify="space-between" mb={6} align="center">
              <Heading size="lg">Clients</Heading>
              <Button colorScheme="blue" onClick={onClientModalOpen}>Add Client</Button>
            </Flex>
            <MotionBox
              overflowX="auto"
              bg={currentColors.tableBg}
              p={4}
              rounded="lg"
              shadow="sm"
              animate={{ backgroundColor: currentColors.tableBg }}
              transition={{ duration: 0.5 }}
            >
              <Table variant="simple">
                <Thead>
                  <Tr bg={currentColors.tableHeaderClients}>
                    <Th>ID</Th>
                    <Th>Telegram ID</Th>
                    <Th>Username</Th>
                    <Th>Full Name</Th>
                  </Tr>
                </Thead>
                <Tbody>
                  {clients.map((c) => (
                    <MotionTr
                      key={c.id}
                      whileHover={{ backgroundColor: currentColors.tableHover }}
                      transition={{ duration: 0.3 }}
                    >
                      <MotionTd>{c.id}</MotionTd>
                      <MotionTd>{c.telegram_id}</MotionTd>
                      <MotionTd>{c.username}</MotionTd>
                      <MotionTd>{c.full_name}</MotionTd>
                    </MotionTr>
                  ))}
                </Tbody>
              </Table>
            </MotionBox>
          </>
        )}

        {activeTab === "projects" && (
          <>
            <Flex justify="space-between" mb={6} align="center">
              <Heading size="lg">Projects</Heading>
              <Button colorScheme="teal" onClick={onProjectModalOpen}>Add Project</Button>
            </Flex>
            <MotionBox
              overflowX="auto"
              bg={currentColors.tableBg}
              p={4}
              rounded="lg"
              shadow="sm"
              animate={{ backgroundColor: currentColors.tableBg }}
              transition={{ duration: 0.5 }}
            >
              <Table variant="simple">
                <Thead>
                  <Tr bg={currentColors.tableHeaderProjects}>
                    <Th>ID</Th>
                    <Th>Client ID</Th>
                    <Th>Type</Th>
                    <Th>Status</Th>
                  </Tr>
                </Thead>
                <Tbody>
                  {projects.map((p) => (
                    <MotionTr
                      key={p.id}
                      whileHover={{ backgroundColor: colorMode === "light" ? "#e6fffa" : "#2a4365" }}
                      transition={{ duration: 0.3 }}
                    >
                      <MotionTd>{p.id}</MotionTd>
                      <MotionTd>{p.client_id}</MotionTd>
                      <MotionTd>{p.project_type}</MotionTd>
                      <MotionTd>
                        <MotionBadge colorScheme={p.status === "active" ? "green" : "red"}>
                          {p.status}
                        </MotionBadge>
                      </MotionTd>
                    </MotionTr>
                  ))}
                </Tbody>
              </Table>
            </MotionBox>
          </>
        )}
      </MotionBox>
    </MotionBox>
  );
}

export default App;
