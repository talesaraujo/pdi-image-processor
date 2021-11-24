import { useState, useEffect, useRef } from 'react'
import { Navbar, Container, Nav, NavDropdown, Form } from 'react-bootstrap'
import { imageUpload } from '../../services/imageUpload'

export function MenuBar() {

    const [image, setImage] = useState(null)
    const isMounted = useRef(false);

    useEffect(() => {
        if (isMounted.current) {
            console.log(image)
            imageUpload(image)
        }
        else {
            isMounted.current = true
        }
    }, [image])

    return (
        <>
        <Navbar bg="light" variant="light" expand="lg">
            <Container>
            <Navbar.Brand href="#home">Image Processor</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="me-auto">

                <NavDropdown title="File" id="basic-dropdown-1">
                    <NavDropdown.Item href="#action/3.1">
                        <Form.Control type="file" size="sm" onChange={(e) => setImage(e.target.files[0])} />
                    </NavDropdown.Item>
                    <NavDropdown.Item href="#action/3.2">Save</NavDropdown.Item>
                    <NavDropdown.Item href="#action/3.3">Save As</NavDropdown.Item>
                    <NavDropdown.Item href="#action/3.4">Undo</NavDropdown.Item>
                </NavDropdown>

                <NavDropdown title="Edit" id="basic-dropdown-2">
                    <NavDropdown.Item href="#action/3.1">Redo</NavDropdown.Item>
                    <NavDropdown.Item href="#action/3.2">Undo</NavDropdown.Item>
                    <NavDropdown.Item href="#action/3.3">Save As</NavDropdown.Item>
                    <NavDropdown.Item href="#action/3.4">Undo</NavDropdown.Item>
                </NavDropdown>
                    
                <NavDropdown title="Intensity" id="basic-dropdown-3">
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
