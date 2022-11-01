// +build state

package main

import (
	"errors"
	"fmt"
)

type State interface {
	fmt.Stringer

	Open() error
	Read() error
	Write() error
	Close() error
}

type Connection struct {
	state State
}

type OpenConnection struct {
	conn *Connection
}

type CloseConnection struct {
	conn *Connection
}

var _ State = (*Connection)(nil)

func NewConnection() *Connection {
	conn := &Connection{}
	closeConn := &CloseConnection{conn}
	conn.state = closeConn

	return conn

}

func (c *Connection) String() string {
	return c.state.String()
}

func (c *Connection) Open() error {
	return c.state.Open()
}

func (c *Connection) Read() error {
	return c.state.Read()
}

func (c *Connection) Write() error {
	return c.state.Write()
}

func (c *Connection) Close() error {
	return c.state.Close()
}

var _ State = (*OpenConnection)(nil)

func (c *OpenConnection) String() string {
	return "Open"
}

func (c *OpenConnection) Open() error {
	return errors.New("Connection already open")
}

func (c *OpenConnection) Read() error {
	fmt.Println("reading")
	return nil
}

func (c *OpenConnection) Write() error {
	fmt.Println("writing")
	return nil
}

func (c *OpenConnection) Close() error {
	c.conn.state = &CloseConnection{
		conn: c.conn,
	}

	return nil
}

var _ State = (*CloseConnection)(nil)

func (c *CloseConnection) String() string {
	return "Close"
}

func (c *CloseConnection) Open() error {
	c.conn.state = &OpenConnection{
		conn: c.conn,
	}

	return nil
}

func (c *CloseConnection) Read() error {
	return errors.New("connection closed")
}

func (c *CloseConnection) Write() error {
	return errors.New("connection closed")
}

func (c *CloseConnection) Close() error {
	return errors.New("connection closed")
}

func main() {
	c := NewConnection()
	fmt.Println(c) // close

	c.Open()
	fmt.Println(c) // open

	c.Write()
	c.Read()

	c.Close()
	fmt.Println(c) // close

	if err := c.Read(); err != nil {
		panic(err) // panic
	}
}
