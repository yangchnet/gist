// +build accesser

package main

import "fmt"

type Visitor interface {
	VisitA(e *ElementA)
	VisitB(e *ElementB)
}

type VisitorA struct {
}

func (v *VisitorA) VisitA(e *ElementA) {
	fmt.Println("visit A")
}

func (v *VisitorA) VisitB(e *ElementB) {
	fmt.Println("visit B")
}

type IElement interface {
	Accept(visit Visitor)
}

type ElementA struct{}

func (e *ElementA) Accept(visit Visitor) {
	visit.VisitA(e)
}

type ElementB struct {
}

func (e *ElementB) Accept(visit Visitor) {
	visit.VisitB(e)
}
