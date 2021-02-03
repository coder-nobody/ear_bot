
class watemplate():
    template=None
    def __init__(self,namespace,t_name,person):
        self.template={
                        "template": {
                            "whatsapp": {
                                "namespace": namespace,
                                "element_name": t_name,
                                "language": {
                                    "policy": "deterministic",
                                    "code": "en"
                                },
                                "components": [
                                    
                                    {
                                        "type": "body",
                                        "parameters": [
                                            {
                                                "type": "text",
                                                "text": person
                                            }
                                        ]
                                    }
                                ]
                            }
                        }
                    }