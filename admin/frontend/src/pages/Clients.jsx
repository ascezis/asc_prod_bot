import React, { useEffect, useState } from "react";
import {
  Box,
  Heading,
  Button,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Input,
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
  FormControl,
  FormLabel,
  IconButton,
  Badge,
  Select,
} from "@chakra-ui/react";
import { EditIcon, DeleteIcon } from "@chakra-ui/icons";
import {
  getClients,
  createClient,
  updateClient,
  deleteClient,
} from "../api/clients";
import { motion } from "framer-motion";

const MotionTr = motion(Tr);

function Clients() {
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [editingClient, setEditingClient] = useState(null);
  const [formData, setFormData] = useState({
    telegram_id: "",
    username: "",
    full_name: "",
  });

  const { isOpen, onOpen, onClose } = useDisclosure();

  useEffect(() => {
    fetchClients();
  }, []);

  const fetchClients = async () => {
    try {
      setLoading(true);
      const params = {};
      if (searchTerm) {
        params.search = searchTerm;
      }
      const data = await getClients(params);
      setClients(data);
    } catch (err) {
      console.error("Ошибка загрузки клиентов:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
    // Debounce поиска
    setTimeout(() => {
      fetchClients();
    }, 500);
  };

  const handleCreate = () => {
    setEditingClient(null);
    setFormData({ telegram_id: "", username: "", full_name: "" });
    onOpen();
  };

  const handleEdit = (client) => {
    setEditingClient(client);
    setFormData({
      telegram_id: client.telegram_id,
      username: client.username || "",
      full_name: client.full_name || "",
    });
    onOpen();
  };

  const handleSave = async () => {
    try {
      if (editingClient) {
        await updateClient(editingClient.id, formData);
      } else {
        await createClient(formData);
      }
      onClose();
      fetchClients();
    } catch (err) {
      console.error("Ошибка сохранения:", err);
      alert(err.response?.data?.detail || "Ошибка сохранения");
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Вы уверены, что хотите удалить этого клиента?")) {
      return;
    }
    try {
      await deleteClient(id);
      fetchClients();
    } catch (err) {
      console.error("Ошибка удаления:", err);
      alert(err.response?.data?.detail || "Ошибка удаления");
    }
  };

  if (loading && clients.length === 0) {
    return (
      <Flex justify="center" align="center" minH="50vh">
        <Spinner size="xl" />
      </Flex>
    );
  }

  return (
    <Box>
      <Flex justify="space-between" align="center" mb={6}>
        <Heading size="lg">👥 Clients</Heading>
        <Button colorScheme="blue" onClick={handleCreate}>
          + Add Client
        </Button>
      </Flex>

      <Flex mb={4} gap={4}>
        <Input
          placeholder="Поиск по username или имени..."
          value={searchTerm}
          onChange={handleSearch}
          maxW="400px"
        />
      </Flex>

      <Box
        overflowX="auto"
        bg="white"
        _dark={{ bg: "gray.800" }}
        p={4}
        rounded="lg"
        shadow="sm"
      >
        <Table variant="simple">
          <Thead>
            <Tr>
              <Th>ID</Th>
              <Th>Telegram ID</Th>
              <Th>Username</Th>
              <Th>Full Name</Th>
              <Th>Проектов</Th>
              <Th>Действия</Th>
            </Tr>
          </Thead>
          <Tbody>
            {clients.map((client) => (
              <MotionTr
                key={client.id}
                whileHover={{ bg: "gray.50" }}
                _dark={{ whileHover: { bg: "gray.700" } }}
              >
                <Td>{client.id}</Td>
                <Td>{client.telegram_id}</Td>
                <Td>@{client.username || "—"}</Td>
                <Td>{client.full_name || "—"}</Td>
                <Td>
                  <Badge colorScheme="blue">{client.projects_count || 0}</Badge>
                </Td>
                <Td>
                  <IconButton
                    icon={<EditIcon />}
                    size="sm"
                    mr={2}
                    onClick={() => handleEdit(client)}
                    aria-label="Edit"
                  />
                  <IconButton
                    icon={<DeleteIcon />}
                    size="sm"
                    colorScheme="red"
                    onClick={() => handleDelete(client.id)}
                    aria-label="Delete"
                  />
                </Td>
              </MotionTr>
            ))}
          </Tbody>
        </Table>
      </Box>

      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>
            {editingClient ? "Редактировать клиента" : "Создать клиента"}
          </ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <FormControl mb={4}>
              <FormLabel>Telegram ID</FormLabel>
              <Input
                type="number"
                value={formData.telegram_id}
                onChange={(e) =>
                  setFormData({ ...formData, telegram_id: e.target.value })
                }
                required
              />
            </FormControl>
            <FormControl mb={4}>
              <FormLabel>Username</FormLabel>
              <Input
                value={formData.username}
                onChange={(e) =>
                  setFormData({ ...formData, username: e.target.value })
                }
              />
            </FormControl>
            <FormControl>
              <FormLabel>Full Name</FormLabel>
              <Input
                value={formData.full_name}
                onChange={(e) =>
                  setFormData({ ...formData, full_name: e.target.value })
                }
              />
            </FormControl>
          </ModalBody>
          <ModalFooter>
            <Button variant="ghost" mr={3} onClick={onClose}>
              Отмена
            </Button>
            <Button colorScheme="blue" onClick={handleSave}>
              Сохранить
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </Box>
  );
}

export default Clients;
