import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import {
  AppBar,
  Box,
  Container,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
} from '@mui/material'
import {
  People,
  ViewInAr,
  Inventory,
  RequestQuote,
  PrecisionManufacturing,
} from '@mui/icons-material'
import Customers from './pages/Customers'
import Materials from './pages/Materials'
import Machines from './pages/Machines'
import Parts from './pages/Parts'
import QuoteBuilder from './pages/QuoteBuilder'
import QuoteView from './pages/QuoteView'
import Quotes from './pages/Quotes'

const drawerWidth = 240

const menuItems = [
  { text: 'Quotes', icon: <RequestQuote />, path: '/quotes' },
  { text: 'New Quote', icon: <RequestQuote />, path: '/quotes/new' },
  { text: 'Customers', icon: <People />, path: '/customers' },
  { text: 'Parts', icon: <ViewInAr />, path: '/parts' },
  { text: 'Materials', icon: <Inventory />, path: '/materials' },
  { text: 'Machines', icon: <PrecisionManufacturing />, path: '/machines' },
]

function App() {
  return (
    <BrowserRouter>
      <Box sx={{ display: 'flex' }}>
        <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
          <Toolbar>
            <PrecisionManufacturing sx={{ mr: 2 }} />
            <Typography variant="h6" noWrap component="div">
              CNC Quoting System
            </Typography>
          </Toolbar>
        </AppBar>

        <Drawer
          variant="permanent"
          sx={{
            width: drawerWidth,
            flexShrink: 0,
            '& .MuiDrawer-paper': { width: drawerWidth, boxSizing: 'border-box' },
          }}
        >
          <Toolbar />
          <Box sx={{ overflow: 'auto' }}>
            <List>
              {menuItems.map((item) => (
                <ListItem key={item.text} disablePadding>
                  <ListItemButton component={Link} to={item.path}>
                    <ListItemIcon>{item.icon}</ListItemIcon>
                    <ListItemText primary={item.text} />
                  </ListItemButton>
                </ListItem>
              ))}
            </List>
          </Box>
        </Drawer>

        <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
          <Toolbar />
          <Container maxWidth="xl">
            <Routes>
              <Route path="/" element={<QuoteBuilder />} />
              <Route path="/quotes" element={<Quotes />} />
              <Route path="/quotes/new" element={<QuoteBuilder />} />
              <Route path="/quotes/:id" element={<QuoteView />} />
              <Route path="/customers" element={<Customers />} />
              <Route path="/materials" element={<Materials />} />
              <Route path="/machines" element={<Machines />} />
              <Route path="/parts" element={<Parts />} />
            </Routes>
          </Container>
        </Box>
      </Box>
    </BrowserRouter>
  )
}

export default App
