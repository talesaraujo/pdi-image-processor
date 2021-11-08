import { Navbar, Container, Nav, NavDropdown } from 'react-bootstrap'

export function MenuBar() {
    return (
        <>
        <Navbar bg="light" variant="light" expand="lg">
            <Container>
            <Navbar.Brand href="#home">Image Processor</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="me-auto">

                <NavDropdown title="File" id="basic-dropdown-1">
                    <NavDropdown.Item href="#action/3.1">Open</NavDropdown.Item>
                    <NavDropdown.Item href="#action/3.2">Save</NavDropdown.Item>
                    <NavDropdown.Item href="#action/3.3">Save As</NavDropdown.Item>
                    <NavDropdown.Item href="#action/3.4">Undo</NavDropdown.Item>
                </NavDropdown>

                <NavDropdown title="Edit" dropdownId="basic-dropdown-2">
                    <NavDropdown.Item href="#action/3.1">Redo</NavDropdown.Item>
                    <NavDropdown.Item href="#action/3.2">Undo</NavDropdown.Item>
                    <NavDropdown.Item href="#action/3.3">Save As</NavDropdown.Item>
                    <NavDropdown.Item href="#action/3.4">Undo</NavDropdown.Item>
                </NavDropdown>
                    
                <NavDropdown title="Intensity" dropdownId="basic-dropdown-3">
                    <NavDropdown.Item href="#action/3.1">Negative</NavDropdown.Item>
                    <NavDropdown.Item href="#action/3.2">Brightness</NavDropdown.Item>
                    <NavDropdown.Item href="#action/3.3">Gamma Transform</NavDropdown.Item>
                    <NavDropdown.Item href="#action/3.4">Log Transform</NavDropdown.Item>
                </NavDropdown>

                </Nav>
            </Navbar.Collapse>
            </Container>
        </Navbar>
        </>
    )
}
