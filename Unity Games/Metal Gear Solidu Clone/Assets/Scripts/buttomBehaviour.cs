using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class buttomBehaviour : MonoBehaviour
{
    public GameObject gameManager;

    private void OnTriggerEnter(Collider other)
    {
        gameManager.GetComponent<gameManagerBehaviour>().OpenDoor();
        Destroy(gameObject);

    }
}
