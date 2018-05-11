using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Interactable : MonoBehaviour
{

    public float radius = 3f;
    public Transform interactionTransform;// isso vai ser usado nas proximas aulas. Serve para setar comportamentos diferentes
                                          //para interactables diferentes. Como no caso de um baú, que so pode ser acessado
                                           //quando o player estiver na frente


    bool isFocus = false;
    Transform player;
    bool hasInteracted = false;


    //virtual pra dar override depois 
    public virtual void Interact()
    {
        Debug.Log("interact");

    }
    private void Update()
    {
        if(isFocus && !hasInteracted)
        {

            //float distance = Vector3.Distance(player.position, transform.position);
            float distance = Vector3.Distance(player.position, interactionTransform.position);

            //esse 1.2 foi pra resolver o bug de parada. As vezes ele para um pouquinho antes. Erro de precisão.
            if (distance<= radius*1.2f)
            {
                Interact();
                hasInteracted = true;
            }
        }
    }
    public void OnFocused(Transform playerTransform)
    {
        isFocus = true;
        player = playerTransform;
        hasInteracted = false;
    }

    public void OnDeFocused()
    {
        isFocus = false;
        hasInteracted = false;
    }
    private void OnDrawGizmosSelected()
    {
        if (interactionTransform == null)
            interactionTransform = transform;// garante que nao tenha nenhum erro no caso detransformada nao selecionada 
        Gizmos.color = Color.yellow;
        Gizmos.DrawWireSphere(interactionTransform.position, radius);
    }

}
