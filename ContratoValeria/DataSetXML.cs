using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

using System.Runtime.Serialization;
using System.ServiceModel;
using System.ServiceModel.Web;

namespace Zuliaworks.Netzuela.Paris.ContratoValeria
{
	// Esta informacion es empleada por el servidor y los clientes
    [DataContract]
    public class DataSetXML
    {
        [DataMember]
        public string EsquemaXML { get; set; }
        [DataMember]
        public string XML { get; set; }
    }
}
