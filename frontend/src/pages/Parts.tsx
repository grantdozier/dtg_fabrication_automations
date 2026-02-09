import { useQuery } from '@tanstack/react-query'
import {
  Box,
  Card,
  CardContent,
  Chip,
  Grid,
  Typography,
} from '@mui/material'
import { api } from '../api/client'

export default function Parts() {
  const { data: parts = [], isLoading } = useQuery({
    queryKey: ['parts'],
    queryFn: api.getParts,
  })

  if (isLoading) return <Typography>Loading...</Typography>

  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 3 }}>
        Parts
      </Typography>

      <Grid container spacing={2}>
        {parts.map((part) => (
          <Grid item xs={12} md={6} lg={4} key={part.id}>
            <Card>
              <CardContent>
                <Typography variant="h6">{part.part_number}</Typography>
                {part.description && (
                  <Typography color="text.secondary" sx={{ mb: 1 }}>
                    {part.description}
                  </Typography>
                )}
                <Typography variant="body2">
                  Stock Weight: {part.stock_weight_lb} lb
                </Typography>
                <Typography variant="body2">
                  Scrap Factor: {(part.scrap_factor * 100).toFixed(0)}%
                </Typography>
                <Box sx={{ mt: 2 }}>
                  <Typography variant="subtitle2" sx={{ mb: 1 }}>
                    Operations ({part.operations.length}):
                  </Typography>
                  {part.operations.map((op) => (
                    <Chip
                      key={op.id}
                      label={op.name}
                      size="small"
                      sx={{ mr: 0.5, mb: 0.5 }}
                    />
                  ))}
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  )
}
