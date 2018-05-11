using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;

[RequireComponent(typeof(PlayerMotor))]
public class playerController : MonoBehaviour
{
    Camera cam;
    PlayerMotor motor;



    public LayerMask movementMask;
    public LayerMask interactable;
    public Interactable focus;


    public int range = 100;




	// Use this for initialization
	void Start ()
    {
        cam = Camera.main;
        motor = GetComponent<PlayerMotor>();
    }
	
	// Update is called once per frame
	void Update ()
    {
        //checa se o clic naoé na UI
        if (EventSystem.current.IsPointerOverGameObject())
            return;
        if (Input.GetMouseButtonDown(0))
        {
            //atira um raio da posicao da camera para a posicao do mouse.
            Ray ray = cam.ScreenPointToRay(Input.mousePosition);

            RaycastHit hit;
            if(Physics.Raycast(ray,out hit,range,movementMask))
            {
                // move our player to what we hit
                motor.MoveToPoint(hit.point);

                //stop focusing any objetcts
                RemoveFocus();
            }
        }


        if (Input.GetMouseButtonDown(1))
        {
            //atira um raio da posicao da camera para a posicao do mouse.
            Ray ray = cam.ScreenPointToRay(Input.mousePosition);

            RaycastHit hit;
            if (Physics.Raycast(ray, out hit, range, interactable))
            {
                //check if hit interactable
                Interactable interactable = hit.collider.GetComponent<Interactable>();
                
                //set focus
                if(interactable != null)
                {
                    SetFocus(interactable);
                }
            }
        }
    }

    void SetFocus(Interactable newFocus)
    {

        //para caso seja outro focus (clica num e depois clica noutro)
        if (newFocus != focus)
        {
            if(focus!=null)
                focus.OnDeFocused();

            focus = newFocus;
            focus.OnFocused(transform);
            motor.FollowTarget(newFocus);
        }


    }

    void RemoveFocus()
    {
        if (focus != null)
            focus.OnDeFocused();


        focus = null;
        motor.StopFollowingTarget();
    }
}
