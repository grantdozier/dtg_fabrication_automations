import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  Box,
  Button,
  Card,
  CardContent,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Grid,
  TextField,
  Typography,
} from '@mui/material'
import { Add } from '@mui/icons-material'
import { api } from '../api/client'

export default function Materials() {
  const [open, setOpen] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    cost_per_lb: '',
    density_lb_in3: '0.283',
    description: '',
  })
  const queryClient = useQueryClient()

  const { data: materials = [], isLoading } = useQuery({
    queryKey: ['materials'],
    queryFn: api.getMaterials,
  })

  const createMutation = useMutation({
    mutationFn: api.createMaterial,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['materials'] })
      setOpen(false)
      setFormData({ name: '', cost_per_lb: '', density_lb_in3: '0.283', description: '' })
    },
  })

  const handleSubmit = () => {
    createMutation.mutate({
      name: formData.name,
      cost_per_lb: parseFloat(formData.cost_per_lb),
      density_lb_in3: parseFloat(formData.density_lb_in3),
      description: formData.description,
    })
  }

  if (isLoading) return <Typography>Loading...</Typography>

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Materials</Typography>
        <Button variant="contained" startIcon={<Add />} onClick={() => setOpen(true)}>
          Add Material
        </Button>
      </Box>

      <Grid container spacing={2}>
        {materials.map((material) => (
          <Grid item xs={12} md={6} lg={4} key={material.id}>
            <Card>
              <CardContent>
                <Typography variant="h6">{material.name}</Typography>
                <Typography color="text.secondary">
                  ${material.cost_per_lb.toFixed(2)}/lb
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Density: {material.density_lb_in3.toFixed(4)} lb/in³
                </Typography>
                {material.description && (
                  <Typography variant="body2" sx={{ mt: 1 }}>
                    {material.description}
                  </Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Dialog open={open} onClose={() => setOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Add New Material</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
            <TextField
              label="Material Name"
              required
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            />
            <TextField
              label="Cost per Pound ($)"
              type="number"
              required
              value={formData.cost_per_lb}
              onChange={(e) => setFormData({ ...formData, cost_per_lb: e.target.value })}
            />
            <TextField
              label="Density (lb/in³)"
              type="number"
              required
              value={formData.density_lb_in3}
              onChange={(e) => setFormData({ ...formData, density_lb_in3: e.target.value })}
            />
            <TextField
              label="Description"
              multiline
              rows={2}
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button
            onClick={handleSubmit}
            variant="contained"
            disabled={!formData.name || !formData.cost_per_lb}
          >
            Create
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}
