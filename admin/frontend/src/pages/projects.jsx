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
  Textarea,
} from "@chakra-ui/react";
import { EditIcon, DeleteIcon } from "@chakra-ui/icons";
import {
  getProjects,
  createProject,
  updateProject,
  deleteProject,
} from "../api/projects";
import { getClients } from "../api/clients";
import { motion } from "framer-motion";

const MotionTr = motion(Tr);

function Projects() {
  const [projects, setProjects] = useState([]);
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [editingProject, setEditingProject] = useState(null);
  const [formData, setFormData] = useState({
    client_id: "",
    project_type: "",
    duration_raw: "",
    duration_final: "",
    services: [],
    deadline: "",
    budget: "",
    source_links: "",
    style_examples: "",
    additional_notes: "",
    status: "new",
  });

  const { isOpen, onOpen, onClose } = useDisclosure();

  useEffect(() => {
    fetchProjects();
    fetchClients();
  }, []);

  const fetchProjects = async () => {
    try {
      setLoading(true);
      const params = {};
      if (searchTerm) {
        params.search = searchTerm;
      }
      if (statusFilter) {
        params.status = statusFilter;
      }
      const data = await getProjects(params);
      setProjects(data);
    } catch (err) {
      console.error("Ошибка загрузки проектов:", err);
    } finally {
      setLoading(false);
    }
  };

  const fetchClients = async () => {
    try {
      const data = await getClients();
      setClients(data);
    } catch (err) {
      console.error("Ошибка загрузки клиентов:", err);
    }
  };

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
    setTimeout(() => {
      fetchProjects();
    }, 500);
  };

  const handleStatusFilter = (e) => {
    setStatusFilter(e.target.value);
    setTimeout(() => {
      fetchProjects();
    }, 100);
  };

  const handleCreate = () => {
    setEditingProject(null);
    setFormData({
      client_id: "",
      project_type: "",
      duration_raw: "",
      duration_final: "",
      services: [],
      deadline: "",
      budget: "",
      source_links: "",
      style_examples: "",
      additional_notes: "",
      status: "new",
    });
    onOpen();
  };

  const handleEdit = (project) => {
    setEditingProject(project);
    setFormData({
      client_id: project.client_id,
      project_type: project.project_type || "",
      duration_raw: project.duration_raw || "",
      duration_final: project.duration_final || "",
      services: project.services || [],
      deadline: project.deadline || "",
      budget: project.budget || "",
      source_links: project.source_links || "",
      style_examples: project.style_examples || "",
      additional_notes: project.additional_notes || "",
      status: project.status || "new",
    });
    onOpen();
  };

  const handleSave = async () => {
    try {
      const data = {
        ...formData,
        client_id: parseInt(formData.client_id),
        services: Array.isArray(formData.services)
          ? formData.services
          : formData.services.split(",").map((s) => s.trim()),
      };
      if (editingProject) {
        await updateProject(editingProject.id, data);
      } else {
        await createProject(data);
      }
      onClose();
      fetchProjects();
    } catch (err) {
      console.error("Ошибка сохранения:", err);
      alert(err.response?.data?.detail || "Ошибка сохранения");
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Вы уверены, что хотите удалить этот проект?")) {
      return;
    }
    try {
      await deleteProject(id);
      fetchProjects();
    } catch (err) {
      console.error("Ошибка удаления:", err);
      alert(err.response?.data?.detail || "Ошибка удаления");
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      new: "blue",
      in_progress: "yellow",
      completed: "green",
      rejected: "red",
    };
    return colors[status] || "gray";
  };

  if (loading && projects.length === 0) {
    return (
      <Flex justify="center" align="center" minH="50vh">
        <Spinner size="xl" />
      </Flex>
    );
  }

  return (
    <Box>
      <Flex justify="space-between" align="center" mb={6}>
        <Heading size="lg">📁 Projects</Heading>
        <Button colorScheme="teal" onClick={handleCreate}>
          + Add Project
        </Button>
      </Flex>

      <Flex mb={4} gap={4}>
        <Input
          placeholder="Поиск по типу, бюджету, дедлайну..."
          value={searchTerm}
          onChange={handleSearch}
          maxW="400px"
        />
        <Select
          placeholder="Все статусы"
          value={statusFilter}
          onChange={handleStatusFilter}
          maxW="200px"
        >
          <option value="new">Новые</option>
          <option value="in_progress">В работе</option>
          <option value="completed">Завершены</option>
          <option value="rejected">Отклонены</option>
        </Select>
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
              <Th>Client ID</Th>
              <Th>Type</Th>
              <Th>Budget</Th>
              <Th>Deadline</Th>
              <Th>Status</Th>
              <Th>Действия</Th>
            </Tr>
          </Thead>
          <Tbody>
            {projects.map((project) => (
              <MotionTr
                key={project.id}
                whileHover={{ bg: "gray.50" }}
                _dark={{ whileHover: { bg: "gray.700" } }}
              >
                <Td>{project.id}</Td>
                <Td>{project.client_id}</Td>
                <Td>{project.project_type}</Td>
                <Td>{project.budget}</Td>
                <Td>{project.deadline}</Td>
                <Td>
                  <Badge colorScheme={getStatusColor(project.status)}>
                    {project.status}
                  </Badge>
                </Td>
                <Td>
                  <IconButton
                    icon={<EditIcon />}
                    size="sm"
                    mr={2}
                    onClick={() => handleEdit(project)}
                    aria-label="Edit"
                  />
                  <IconButton
                    icon={<DeleteIcon />}
                    size="sm"
                    colorScheme="red"
                    onClick={() => handleDelete(project.id)}
                    aria-label="Delete"
                  />
                </Td>
              </MotionTr>
            ))}
          </Tbody>
        </Table>
      </Box>

      <Modal isOpen={isOpen} onClose={onClose} size="xl">
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>
            {editingProject ? "Редактировать проект" : "Создать проект"}
          </ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <FormControl mb={4}>
              <FormLabel>Client ID</FormLabel>
              <Select
                value={formData.client_id}
                onChange={(e) =>
                  setFormData({ ...formData, client_id: e.target.value })
                }
                required
              >
                <option value="">Выберите клиента</option>
                {clients.map((client) => (
                  <option key={client.id} value={client.id}>
                    {client.full_name || client.username || client.id}
                  </option>
                ))}
              </Select>
            </FormControl>
            <FormControl mb={4}>
              <FormLabel>Project Type</FormLabel>
              <Input
                value={formData.project_type}
                onChange={(e) =>
                  setFormData({ ...formData, project_type: e.target.value })
                }
                required
              />
            </FormControl>
            <Flex gap={4} mb={4}>
              <FormControl>
                <FormLabel>Duration Raw</FormLabel>
                <Input
                  value={formData.duration_raw}
                  onChange={(e) =>
                    setFormData({ ...formData, duration_raw: e.target.value })
                  }
                  required
                />
              </FormControl>
              <FormControl>
                <FormLabel>Duration Final</FormLabel>
                <Input
                  value={formData.duration_final}
                  onChange={(e) =>
                    setFormData({ ...formData, duration_final: e.target.value })
                  }
                  required
                />
              </FormControl>
            </Flex>
            <FormControl mb={4}>
              <FormLabel>Services (через запятую)</FormLabel>
              <Input
                value={
                  Array.isArray(formData.services)
                    ? formData.services.join(", ")
                    : formData.services
                }
                onChange={(e) =>
                  setFormData({ ...formData, services: e.target.value })
                }
                required
              />
            </FormControl>
            <Flex gap={4} mb={4}>
              <FormControl>
                <FormLabel>Deadline</FormLabel>
                <Input
                  value={formData.deadline}
                  onChange={(e) =>
                    setFormData({ ...formData, deadline: e.target.value })
                  }
                  required
                />
              </FormControl>
              <FormControl>
                <FormLabel>Budget</FormLabel>
                <Input
                  value={formData.budget}
                  onChange={(e) =>
                    setFormData({ ...formData, budget: e.target.value })
                  }
                  required
                />
              </FormControl>
            </Flex>
            <FormControl mb={4}>
              <FormLabel>Status</FormLabel>
              <Select
                value={formData.status}
                onChange={(e) =>
                  setFormData({ ...formData, status: e.target.value })
                }
              >
                <option value="new">New</option>
                <option value="in_progress">In Progress</option>
                <option value="completed">Completed</option>
                <option value="rejected">Rejected</option>
              </Select>
            </FormControl>
            <FormControl mb={4}>
              <FormLabel>Source Links</FormLabel>
              <Textarea
                value={formData.source_links}
                onChange={(e) =>
                  setFormData({ ...formData, source_links: e.target.value })
                }
              />
            </FormControl>
            <FormControl mb={4}>
              <FormLabel>Style Examples</FormLabel>
              <Textarea
                value={formData.style_examples}
                onChange={(e) =>
                  setFormData({ ...formData, style_examples: e.target.value })
                }
              />
            </FormControl>
            <FormControl>
              <FormLabel>Additional Notes</FormLabel>
              <Textarea
                value={formData.additional_notes}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    additional_notes: e.target.value,
                  })
                }
              />
            </FormControl>
          </ModalBody>
          <ModalFooter>
            <Button variant="ghost" mr={3} onClick={onClose}>
              Отмена
            </Button>
            <Button colorScheme="teal" onClick={handleSave}>
              Сохранить
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </Box>
  );
}

export default Projects;
